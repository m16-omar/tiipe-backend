from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.shortcuts import redirect

def api_root_view(request):
    accept = request.META.get('HTTP_ACCEPT', '')
    if 'text/html' in accept or '*/*' in accept:
        return redirect('/admin/')

    return JsonResponse({
        'service': 'TIIPE & Novatrix Unified Multi-Tenant Backend Gateway',
        'status': 'online',
        'active_schema': 'public',
        'documentation': {
            'swagger_ui': '/api/docs/',
            'redoc': '/api/redoc/',
            'openapi_json_schema': '/api/schema/',
        },
        'admin_portal': '/admin/',
        'health_check': '/health/',
        'authentication': {
            'login': '/api/v1/auth/login/',
            'register': '/api/v1/auth/register/',
            'profile': '/api/v1/auth/me/',
        },
        'tenants': {
            'list_tenants': '/api/v1/core/tenants/',
            'current_tenant': '/api/v1/core/tenants/current/',
        },
        'usage_note': (
            'To query tenant-specific resources (TIIPE LMS or Novatrix Services), '
            'pass the HTTP header "X-Tenant: tiipe" or "X-Tenant: novatrix", '
            'or access via subdomain (e.g. tiipe.localhost:8000 or novatrix.localhost:8000).'
        )
    })

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'schema': 'public',
        'service': 'TIIPE & Novatrix Master Multi-Tenant Gateway',
        'version': '1.0.0'
    })

urlpatterns = [
    path('', api_root_view, name='public-api-root'),
    path('admin/', admin.site.urls),
    path('health/', health_check, name='public-health-check'),
    
    # OpenAPI 3.0 Documentation for Public Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='public-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='public-schema'), name='public-swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='public-schema'), name='public-redoc'),
    
    # Global User Authentication & Profile
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/core/', include('apps.core.urls')),
]
