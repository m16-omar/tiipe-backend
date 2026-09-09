from decimal import Decimal
from rest_framework import viewsets, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Donation, DonationAllocation, PaymentTransaction, Invoice, WebhookLog
from .serializers import (
    DonationSerializer, DonationAllocationSerializer,
    PaymentTransactionSerializer, InvoiceSerializer, WebhookLogSerializer
)
from apps.core.permissions import IsTenantAdmin

class DonationViewSet(viewsets.ModelViewSet):
    """
    Handles charitable donations for TIIPE 501(c)(3) initiatives.
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'frequency', 'fund_allocation', 'gateway']
    ordering_fields = ['created_at', 'amount']

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsTenantAdmin()]

    def perform_create(self, serializer):
        donation = serializer.save()
        
        # Nonprofit processing fee calculation (~2.2% + $0.30)
        gross = donation.amount
        fee = (gross * Decimal('0.022')) + Decimal('0.30')
        net = gross - fee
        if net < Decimal('0.00'):
            net = Decimal('0.00')

        donation.status = 'successful'
        donation.gateway_fee = fee
        donation.net_amount = net
        donation.tax_receipt_pdf_url = f"https://impactinstituteglobal.org/receipts/{donation.donation_id}.pdf"
        donation.save()

        # Create Ledger Sub-Account Allocation Record
        DonationAllocation.objects.create(
            donation=donation,
            fund_name=donation.get_fund_allocation_display(),
            gross_amount=gross,
            net_credited_amount=net
        )


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_purpose']
    ordering_fields = ['created_at', 'amount']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsTenantAdmin()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    lookup_field = 'invoice_number'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.filter(user=user) | Invoice.objects.filter(recipient_email=user.email)


class WebhookReceiverView(APIView):
    """
    Receives and logs incoming payment webhook events from Stripe/Paystack.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, gateway):
        payload = request.data
        event_type = payload.get('type') or payload.get('event') or 'unknown'

        log = WebhookLog.objects.create(
            gateway=gateway,
            event_type=event_type,
            payload=payload,
            is_processed=True
        )

        return Response({
            'success': True,
            'message': f'{gateway} webhook received successfully',
            'log_id': log.id
        }, status=status.HTTP_200_OK)
