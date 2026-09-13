from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import ClientTenant, Domain

@admin.register(ClientTenant)
class ClientTenantAdmin(TenantAdminMixin, ModelAdmin):
    list_display = ('name', 'schema_name', 'show_brand', 'show_status', 'created_on')
    search_fields = ('name', 'schema_name', 'brand_type', 'tagline')
    list_filter = ('brand_type', 'is_active')
    list_filter_submit = True
    
    @display(
        description="Brand",
        label={
            "tiipe": "info",
            "novatrix": "warning",
        }
    )
    def show_brand(self, obj):
        return obj.brand_type

    @display(
        description="Active",
        boolean=True
    )
    def show_status(self, obj):
        return obj.is_active


@admin.register(Domain)
class DomainAdmin(ModelAdmin):
    list_display = ('domain', 'tenant', 'show_primary')
    search_fields = ('domain', 'tenant__name')
    list_filter = ('is_primary',)
    list_filter_submit = True

    @display(
        description="Primary",
        boolean=True
    )
    def show_primary(self, obj):
        return obj.is_primary

