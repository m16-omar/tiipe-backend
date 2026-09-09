from django.contrib import admin
from .models import Donation, DonationAllocation, PaymentTransaction, Invoice, WebhookLog

class DonationAllocationInline(admin.StackedInline):
    model = DonationAllocation
    can_delete = False


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'donor_email', 'amount', 'frequency', 'fund_allocation', 'status', 'created_at')
    list_filter = ('status', 'frequency', 'fund_allocation', 'gateway')
    search_fields = ('donor_name', 'donor_email', 'transaction_reference')
    inlines = [DonationAllocationInline]


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_ref', 'user', 'amount', 'currency', 'payment_purpose', 'status', 'created_at')
    list_filter = ('status', 'payment_purpose', 'gateway')
    search_fields = ('transaction_ref', 'user__email')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'recipient_name', 'recipient_email', 'total_amount', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    search_fields = ('invoice_number', 'recipient_name', 'recipient_email', 'recipient_organization')


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'event_type', 'is_processed', 'received_at')
    list_filter = ('gateway', 'is_processed')
    search_fields = ('event_type', 'gateway')
