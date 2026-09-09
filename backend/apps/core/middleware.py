from django.db import connection
from django.http import Http404, HttpResponseNotFound
from django.conf import settings
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.utils import get_public_schema_name, get_tenant_model, get_tenant_domain_model

class TenantHeaderAndHostMiddleware(TenantMainMiddleware):
    """
    Custom Tenant Middleware for TIIPE & Novatrix.
    Detects tenant via:
    1. HTTP header 'X-Tenant' (used by mobile apps and frontend API clients)
    2. Request hostname / subdomain matching (django-tenants Domain table)
    3. Fallback to public schema for global endpoints.
    """

    def get_tenant(self, domain_model, hostname):
        # We will override process_request for full header + host support
        return super().get_tenant(domain_model, hostname)

    def process_request(self, request):
        # Ensure database connection is ready
        connection.set_schema_to_public()
        
        tenant_model = get_tenant_model()
        domain_model = get_tenant_domain_model()
        
        # 1. Check for custom X-Tenant header (mobile apps, web client override)
        header_tenant = request.headers.get('X-Tenant') or request.META.get('HTTP_X_TENANT')
        tenant = None
        
        if header_tenant:
            header_tenant_slug = header_tenant.strip().lower()
            try:
                tenant = tenant_model.objects.filter(
                    is_active=True
                ).filter(
                    schema_name=header_tenant_slug
                ).first() or tenant_model.objects.filter(
                    brand_type=header_tenant_slug
                ).first()
            except Exception:
                tenant = None

        # 2. If no header, resolve by request.get_host()
        if not tenant:
            hostname = self.hostname_from_request(request)
            try:
                domain = domain_model.objects.select_related('tenant').get(domain=hostname)
                tenant = domain.tenant
            except domain_model.DoesNotExist:
                # Check without port if present
                clean_host = hostname.split(':')[0]
                try:
                    domain = domain_model.objects.select_related('tenant').get(domain=clean_host)
                    tenant = domain.tenant
                except domain_model.DoesNotExist:
                    # Fallback to public tenant or default
                    tenant = None

        # 3. If still no tenant or requested public host, set public schema
        if not tenant:
            try:
                tenant = tenant_model.objects.get(schema_name=get_public_schema_name())
            except tenant_model.DoesNotExist:
                # System booting before seed
                tenant = None

        if tenant:
            request.tenant = tenant
            connection.set_tenant(request.tenant)
            self.setup_url_routing(request)
        else:
            connection.set_schema_to_public()
            request.tenant = None

    def setup_url_routing(self, request):
        public_schema_name = get_public_schema_name()
        if request.tenant and request.tenant.schema_name == public_schema_name:
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
        else:
            request.urlconf = settings.ROOT_URLCONF
