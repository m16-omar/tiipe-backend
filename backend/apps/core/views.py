from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ClientTenant
from .serializers import ClientTenantSerializer

class TenantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public API endpoint to query active tenants and their branding configuration.
    """
    queryset = ClientTenant.objects.filter(is_active=True).exclude(schema_name='public')
    serializer_class = ClientTenantSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def current(self, request):
        tenant = getattr(request, 'tenant', None)
        if tenant:
            serializer = self.get_serializer(tenant)
            return Response({'success': True, 'tenant': serializer.data})
        return Response({'success': False, 'message': 'Public context or tenant not detected'}, status=404)
