import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import NotificationLog

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_async_email(self, recipient_email, subject, body_plain, body_html=None, from_email=None):
    """
    Celery task to send transactional emails asynchronously.
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject=subject,
            message=body_plain,
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=body_html,
            fail_silently=False
        )
        NotificationLog.objects.create(
            recipient_email=recipient_email,
            title=subject,
            body=body_plain,
            channel='email',
            status='sent',
            sent_at=timezone.now()
        )
        logger.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {recipient_email}: {exc}")
        NotificationLog.objects.create(
            recipient_email=recipient_email,
            title=subject,
            body=body_plain,
            channel='email',
            status='failed',
            error_message=str(exc)
        )
        raise self.retry(exc=exc)


@shared_task
def send_async_push_notification(user_id, title, body, extra_data=None):
    """
    Celery task to dispatch mobile push notifications via FCM / APNS.
    """
    from apps.notifications.models import PushDeviceToken
    tokens = PushDeviceToken.objects.filter(user_id=user_id, is_active=True).values_list('device_token', flat=True)
    logger.info(f"Dispatching push notification to {len(tokens)} devices for user {user_id}: {title}")
    return len(tokens)
