from rest_framework import serializers
from .models import ClientTenant, Domain

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'domain', 'is_primary')


class ClientTenantSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True, read_only=True)

    class Meta:
        model = ClientTenant
        fields = (
            'id', 'schema_name', 'name', 'brand_type', 'tagline',
            'description', 'primary_color', 'accent_color', 'contact_email',
            'contact_phone', 'is_active', 'domains'
        )
