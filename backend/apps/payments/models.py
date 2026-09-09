import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class Donation(models.Model):
    """
    TIIPE 501(c)(3) Charitable Donation Model with Program Targeted Allocations.
    """
    FREQUENCY_CHOICES = (
        ('one_time', 'One-Time Contribution'),
        ('monthly', 'Monthly Recurring Giving'),
    )
    ALLOCATION_CHOICES = (
        ('general_fund', 'TIIPE General Operations & Impact Fund'),
        ('education_tutoring', 'Academic Tutoring & Student Learning Kits'),
        ('public_health', 'Public Health & Maternal Literacy Outreach'),
        ('civic_outreach', 'Civic Engagement & Policy Research'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('successful', 'Completed & Verified'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    )
    GATEWAY_CHOICES = (
        ('stripe', 'Stripe Payments'),
        ('paypal', 'PayPal Gateway'),
        ('paystack', 'Paystack'),
    )
    donation_id = models.CharField(max_length=60, unique=True, default=uuid.uuid4)
    donor_name = models.CharField(max_length=150)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=50, blank=True)
    donor_address = models.TextField(blank=True, help_text="Used for 501(c)(3) tax receipt generation")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='one_time')
    fund_allocation = models.CharField(max_length=40, choices=ALLOCATION_CHOICES, default='general_fund')
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES, default='stripe')
    transaction_reference = models.CharField(max_length=150, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_receipt_pdf_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Donation ${self.amount} by {self.donor_email} [{self.get_status_display()}]"


class DonationAllocation(models.Model):
    """
    Financial sub-ledger record allocating net funds to specific program budgets.
    """
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='ledger_allocation')
    fund_name = models.CharField(max_length=100)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    net_credited_amount = models.DecimalField(max_digits=12, decimal_places=2)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Allocation: ${self.net_credited_amount} to {self.fund_name}"


class PaymentTransaction(models.Model):
    """
    General commercial payment transactions (Novatrix training course enrollments & client invoices).
    """
    PURPOSE_CHOICES = (
        ('course_enrollment', 'Training Course Enrollment'),
        ('corporate_training', 'Corporate Cohort Training'),
        ('software_milestone', 'Custom Software Development Milestone'),
        ('support_retainer', 'Support & Maintenance Retainer'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_ref = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    payment_purpose = models.CharField(max_length=40, choices=PURPOSE_CHOICES, default='course_enrollment')
    gateway = models.CharField(max_length=30, default='stripe')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.transaction_ref[:10]} - {self.amount} {self.currency} [{self.status}]"


class Invoice(models.Model):
    """
    Itemized invoices generated for corporate clients and training cohorts.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('paid', 'Paid'),
        ('void', 'Void'),
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    recipient_name = models.CharField(max_length=150)
    recipient_email = models.EmailField()
    recipient_organization = models.CharField(max_length=150, blank=True)
    line_items = models.JSONField(default=list, help_text="[{'description': '...', 'quantity': 1, 'unit_price': 100}]")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='issued')
    pdf_download_url = models.URLField(max_length=500, blank=True)
    due_date = models.DateField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.recipient_name} (${self.total_amount})"


class WebhookLog(models.Model):
    """
    Logs raw incoming webhook payloads from Stripe, Paystack, and PayPal for idempotency & audit.
    """
    gateway = models.CharField(max_length=30)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    is_processed = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.gateway} Webhook: {self.event_type} ({self.received_at.strftime('%Y-%m-%d %H:%M')})"
