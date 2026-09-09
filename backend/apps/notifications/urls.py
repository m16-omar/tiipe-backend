from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PushDeviceTokenViewSet, NotificationLogViewSet, EmailTemplateViewSet

router = DefaultRouter()
router.register(r'push-tokens', PushDeviceTokenViewSet, basename='notifications-push-tokens')
router.register(r'logs', NotificationLogViewSet, basename='notifications-logs')
router.register(r'templates', EmailTemplateViewSet, basename='notifications-templates')

urlpatterns = [
    path('', include(router.urls)),
]
