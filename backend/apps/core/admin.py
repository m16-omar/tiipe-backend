from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import ClientTenant, Domain

@admin.register(ClientTenant)
class ClientTenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'brand_type', 'is_active', 'created_on')
    search_fields = ('name', 'schema_name', 'brand_type')
    list_filter = ('brand_type', 'is_active')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain', 'tenant__name')
    list_filter = ('is_primary',)
