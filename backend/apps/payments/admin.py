from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import display
from .models import Donation, DonationAllocation, PaymentTransaction, Invoice, WebhookLog

class DonationAllocationInline(StackedInline):
    model = DonationAllocation
    can_delete = False


@admin.register(Donation)
class DonationAdmin(ModelAdmin):
    list_display = ('donor_name', 'donor_email', 'amount', 'show_frequency', 'show_fund', 'show_status', 'created_at')
    list_filter = ('status', 'frequency', 'fund_allocation', 'gateway')
    list_filter_submit = True
    search_fields = ('donor_name', 'donor_email', 'transaction_reference')
    inlines = [DonationAllocationInline]

    @display(
        description="Status",
        label={
            "succeeded": "success",
            "pending": "warning",
            "failed": "danger",
            "refunded": "secondary",
        }
    )
    def show_status(self, obj):
        return obj.status

    @display(
        description="Frequency",
        label={
            "monthly": "primary",
            "one_time": "info",
        }
    )
    def show_frequency(self, obj):
        return obj.frequency

    @display(
        description="Fund Target",
        label={
            "general": "secondary",
            "education": "success",
            "health": "warning",
            "civic": "info",
        }
    )
    def show_fund(self, obj):
        return obj.fund_allocation


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    list_display = ('transaction_ref', 'user', 'amount', 'currency', 'payment_purpose', 'show_status', 'created_at')
    list_filter = ('status', 'payment_purpose', 'gateway')
    list_filter_submit = True
    search_fields = ('transaction_ref', 'user__email')

    @display(
        description="Status",
        label={
            "succeeded": "success",
            "pending": "warning",
            "failed": "danger",
        }
    )
    def show_status(self, obj):
        return obj.status


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ('invoice_number', 'recipient_name', 'recipient_email', 'total_amount', 'show_status', 'due_date')
    list_filter = ('status', 'due_date')
    list_filter_submit = True
    search_fields = ('invoice_number', 'recipient_name', 'recipient_email', 'recipient_organization')

    @display(
        description="Status",
        label={
            "paid": "success",
            "open": "warning",
            "overdue": "danger",
            "void": "secondary",
        }
    )
    def show_status(self, obj):
        return obj.status


@admin.register(WebhookLog)
class WebhookLogAdmin(ModelAdmin):
    list_display = ('gateway', 'event_type', 'show_processed', 'received_at')
    list_filter = ('gateway', 'is_processed')
    list_filter_submit = True
    search_fields = ('event_type', 'gateway')

    @display(description="Processed", boolean=True)
    def show_processed(self, obj):
        return obj.is_processed

