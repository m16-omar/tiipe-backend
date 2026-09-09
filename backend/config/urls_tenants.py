from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def tenant_api_root(request):
    tenant = getattr(request, 'tenant', None)
    schema = getattr(tenant, 'schema_name', 'unknown')
    brand = getattr(tenant, 'brand_type', 'unknown')
    
    return JsonResponse({
        'tenant_name': getattr(tenant, 'name', 'TIIPE / Novatrix'),
        'brand': brand,
        'schema': schema,
        'status': 'online',
        'documentation': {
            'swagger_ui': '/api/docs/',
            'redoc': '/api/redoc/',
            'openapi_json_schema': '/api/schema/',
        },
        'endpoints': {
            'cms': '/api/v1/cms/',
            'lms': '/api/v1/lms/' if brand == 'tiipe' else 'N/A (TIIPE only)',
            'services': '/api/v1/services/' if brand == 'novatrix' else 'N/A (Novatrix only)',
            'payments': '/api/v1/payments/',
            'notifications': '/api/v1/notifications/',
            'files': '/api/v1/files/',
            'auth': '/api/v1/auth/',
        }
    })

def tenant_health_check(request):
    tenant = getattr(request, 'tenant', None)
    return JsonResponse({
        'status': 'healthy',
        'tenant_schema': getattr(tenant, 'schema_name', 'unknown'),
        'tenant_name': getattr(tenant, 'name', 'unknown'),
        'brand': getattr(tenant, 'brand_type', 'unknown'),
        'version': '1.0.0'
    })

urlpatterns = [
    path('', tenant_api_root, name='tenant-api-root'),
    path('admin/', admin.site.urls),
    path('health/', tenant_health_check, name='tenant-health-check'),
    
    # OpenAPI 3.0 Documentation for Tenant Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='tenant-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='tenant-schema'), name='tenant-swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='tenant-schema'), name='tenant-redoc'),
    
    # Tenant Isolated Business API Endpoints
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/cms/', include('apps.cms.urls')),
    path('api/v1/lms/', include('apps.tiipe_lms.urls')),
    path('api/v1/services/', include('apps.novatrix_services.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/files/', include('apps.files.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
