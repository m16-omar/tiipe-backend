from rest_framework import serializers
from .models import Donation, DonationAllocation, PaymentTransaction, Invoice, WebhookLog

class DonationAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationAllocation
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    fund_allocation_display = serializers.CharField(source='get_fund_allocation_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    ledger_allocation = DonationAllocationSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = (
            'donation_id', 'status', 'gateway_fee', 'net_amount',
            'tax_receipt_pdf_url', 'created_at'
        )


class PaymentTransactionSerializer(serializers.ModelSerializer):
    purpose_display = serializers.CharField(source='get_payment_purpose_display', read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = '__all__'
        read_only_fields = ('transaction_ref', 'created_at')


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class WebhookLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookLog
        fields = '__all__'
