from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PushDeviceToken, NotificationLog, EmailTemplate
from .serializers import PushDeviceTokenSerializer, NotificationLogSerializer, EmailTemplateSerializer
from apps.core.permissions import IsTenantAdmin

class PushDeviceTokenViewSet(viewsets.ModelViewSet):
    """
    Register and manage mobile push notification tokens.
    """
    serializer_class = PushDeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PushDeviceToken.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Update or create token for the authenticated user
        device_token = serializer.validated_data['device_token']
        platform = serializer.validated_data.get('platform', 'android')
        token_obj, created = PushDeviceToken.objects.update_or_create(
            device_token=device_token,
            defaults={
                'user': self.request.user,
                'platform': platform,
                'is_active': True
            }
        )
        return token_obj


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List user notifications.
    """
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return NotificationLog.objects.all()
        return NotificationLog.objects.filter(recipient_user=user) | NotificationLog.objects.filter(recipient_email=user.email)


class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsTenantAdmin]
    lookup_field = 'template_key'
