from django.contrib import admin
from .models import PushDeviceToken, NotificationLog, EmailTemplate

@admin.register(PushDeviceToken)
class PushDeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'is_active', 'updated_at')
    list_filter = ('platform', 'is_active')
    search_fields = ('user__email', 'device_token')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient_email', 'channel', 'status', 'created_at')
    list_filter = ('channel', 'status', 'created_at')
    search_fields = ('title', 'recipient_email', 'recipient_phone')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_key', 'subject', 'is_active')
    search_fields = ('template_key', 'subject')
