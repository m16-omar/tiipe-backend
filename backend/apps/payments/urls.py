from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationViewSet, PaymentTransactionViewSet, InvoiceViewSet, WebhookReceiverView

router = DefaultRouter()
router.register(r'donations', DonationViewSet, basename='payments-donations')
router.register(r'transactions', PaymentTransactionViewSet, basename='payments-transactions')
router.register(r'invoices', InvoiceViewSet, basename='payments-invoices')

urlpatterns = [
    path('webhooks/<str:gateway>/', WebhookReceiverView.as_view(), name='payment-webhook'),
    path('', include(router.urls)),
]
