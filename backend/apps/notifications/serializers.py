from rest_framework import serializers
from .models import PushDeviceToken, NotificationLog, EmailTemplate

class PushDeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushDeviceToken
        fields = ('id', 'device_token', 'platform', 'is_active', 'updated_at')
        read_only_fields = ('updated_at',)


class NotificationLogSerializer(serializers.ModelSerializer):
    channel_display = serializers.CharField(source='get_channel_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = NotificationLog
        fields = '__all__'
        read_only_fields = ('sent_at', 'created_at')


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
