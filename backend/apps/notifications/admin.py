from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import PushDeviceToken, NotificationLog, EmailTemplate

@admin.register(PushDeviceToken)
class PushDeviceTokenAdmin(ModelAdmin):
    list_display = ('user', 'show_platform', 'show_active', 'updated_at')
    list_filter = ('platform', 'is_active')
    list_filter_submit = True
    search_fields = ('user__email', 'device_token')

    @display(
        description="Platform",
        label={
            "ios": "info",
            "android": "success",
            "web": "primary",
        }
    )
    def show_platform(self, obj):
        return obj.platform

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(NotificationLog)
class NotificationLogAdmin(ModelAdmin):
    list_display = ('title', 'recipient_email', 'channel', 'show_status', 'created_at')
    list_filter = ('channel', 'status', 'created_at')
    list_filter_submit = True
    search_fields = ('title', 'recipient_email', 'recipient_phone')

    @display(
        description="Status",
        label={
            "sent": "success",
            "delivered": "info",
            "pending": "warning",
            "failed": "danger",
        }
    )
    def show_status(self, obj):
        return obj.status


@admin.register(EmailTemplate)
class EmailTemplateAdmin(ModelAdmin):
    list_display = ('template_key', 'subject', 'show_active')
    list_filter_submit = True
    search_fields = ('template_key', 'subject')

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active

