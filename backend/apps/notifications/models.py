from django.db import models
from django.conf import settings

class PushDeviceToken(models.Model):
    """
    Push notification tokens registered by Flutter Mobile Apps (iOS & Android) and Web browsers.
    """
    PLATFORM_CHOICES = (
        ('ios', 'Apple iOS Device'),
        ('android', 'Google Android Device'),
        ('web', 'Web Browser Push'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_tokens')
    device_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='android')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.platform} ({self.device_token[:12]}...)"


class NotificationLog(models.Model):
    """
    Audit log of all outbound emails, push notifications, and SMS alerts.
    """
    CHANNEL_CHOICES = (
        ('email', 'Email (SendGrid/SMTP)'),
        ('push', 'Push Notification (Firebase Cloud Messaging)'),
        ('sms', 'SMS (Twilio)'),
        ('in_app', 'In-App Alert'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending Dispatch'),
        ('sent', 'Sent Successfully'),
        ('failed', 'Dispatch Failed'),
    )
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='email')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_channel_display()}] to {self.recipient_email or self.recipient_phone}: {self.title}"


class EmailTemplate(models.Model):
    """
    Customizable transactional email templates per tenant.
    """
    template_key = models.CharField(max_length=100, unique=True, help_text="e.g. 'welcome_email', 'donation_receipt'")
    subject = models.CharField(max_length=255)
    body_html = models.TextField(help_text="HTML template with {{ placeholders }}")
    body_plain = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Template: {self.template_key} ({self.subject})"
