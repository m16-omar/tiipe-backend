import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class ServicePillar(models.Model):
    """
    Novatrix 4 Core Service Pillars:
    1. Custom Software Development
    2. System Implementation & Integration
    3. Technology Training & Workforce Development
    4. Support and System Optimization
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.TextField()
    problem_addressed = models.TextField()
    capabilities = models.JSONField(default=list, help_text="List of specific deliverables/capabilities")
    engagement_types = models.TextField(help_text="e.g. Full build, Modernization, Architecture audit")
    delivery_process = models.JSONField(default=list, help_text="List of process stages (Discover, Define, Design, etc.)")
    faqs = models.JSONField(default=list, help_text="Service-specific FAQs: [{'q': '...', 'a': '...'}]")
    cta_label = models.CharField(max_length=100, default='Discuss Your Project')
    cta_link = models.CharField(max_length=255, default='/consultation')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class IndustrySolution(models.Model):
    """
    Novatrix Industry Verticals (Education, Healthcare, Nonprofits, SMEs, Public Sector, Media).
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    overview = models.TextField()
    common_challenges = models.TextField()
    sample_solutions = models.JSONField(default=list, help_text="List of solutions tailored to this industry")
    compliance_disclaimer = models.CharField(max_length=255, blank=True)
    icon_name = models.CharField(max_length=100, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name


class ProjectCaseStudy(models.Model):
    """
    Novatrix Project Portfolio and Blueprints with transparent status labels.
    """
    STATUS_CHOICES = (
        ('delivered', 'Delivered & Verified'),
        ('in_development', 'In Active Development'),
        ('concept', 'Product Concept / Blueprint'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    client_name = models.CharField(max_length=150, help_text="Client or Product Name (e.g. TIIPE Digital Platform)")
    industry = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='in_development')
    challenge = models.TextField()
    approach = models.TextField()
    solution = models.TextField()
    technology_stack = models.JSONField(default=list, help_text="['Django', 'React', 'PostgreSQL', 'Flutter']")
    training_and_adoption = models.TextField(blank=True, help_text="Training provided to client staff")
    outcomes_achieved = models.TextField(blank=True)
    demo_url = models.URLField(max_length=500, blank=True)
    cover_image_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Project case studies'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"


class TrainingCourse(models.Model):
    """
    Novatrix Training Catalog Courses (Fullstack, Data & AI, Cloud, Business Automation).
    """
    TOPIC_CHOICES = (
        ('web_mobile', 'Web & Mobile Application Engineering'),
        ('data_ai', 'Data Analytics, Engineering & Applied AI'),
        ('cloud_devops', 'Cloud Infrastructure & DevOps'),
        ('business_systems', 'Business Systems Implementation & CRM'),
        ('digital_foundations', 'Digital Literacy & Productivity Foundations'),
    )
    LEVEL_CHOICES = (
        ('beginner', 'Foundational / Beginner'),
        ('intermediate', 'Intermediate / Career Transition'),
        ('advanced', 'Advanced / Senior Specialization'),
    )
    FORMAT_CHOICES = (
        ('live_online', 'Live Online Cohort'),
        ('in_person', 'In-Person Workshop / BootCamp'),
        ('hybrid', 'Hybrid (Online + In-Person)'),
        ('self_paced', 'Self-Paced with Mentor Reviews'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    topic_category = models.CharField(max_length=40, choices=TOPIC_CHOICES, default='web_mobile')
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, default='beginner')
    format = models.CharField(max_length=30, choices=FORMAT_CHOICES, default='live_online')
    duration_weeks = models.PositiveIntegerField(default=8)
    summary = models.TextField()
    target_audience = models.CharField(max_length=255)
    learning_outcomes = models.JSONField(default=list)
    prerequisites = models.TextField(blank=True)
    syllabus_modules = models.JSONField(default=list, help_text="List of curriculum modules and weekly topics")
    hands_on_projects = models.JSONField(default=list, help_text="List of portfolio projects built during training")
    certificate_details = models.CharField(max_length=255, default='Assessed Credential and Verified Digital Certificate')
    price_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_currency = models.CharField(max_length=10, default='USD')
    is_enrollment_open = models.BooleanField(default=True)
    cover_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['topic_category', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"


class TrainingCohort(models.Model):
    """
    Specific cohort dates for training courses.
    """
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='cohorts')
    cohort_name = models.CharField(max_length=100, help_text="e.g. 'Cohort 2026-Q3'")
    start_date = models.DateField()
    end_date = models.DateField()
    schedule_description = models.CharField(max_length=200, help_text="e.g. 'Tuesdays & Thursdays 6pm - 8pm WAT'")
    max_capacity = models.PositiveIntegerField(default=30)
    enrolled_count = models.PositiveIntegerField(default=0)
    is_registration_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.title} - {self.cohort_name} (Starts {self.start_date})"


class ProjectInquiry(models.Model):
    """
    Novatrix structured consultation / project inquiry form submissions.
    """
    SERVICE_CHOICES = (
        ('custom_software', 'Custom Software Development'),
        ('system_implementation', 'System Implementation & Integration'),
        ('systems_integration', 'Systems Integration & APIs'),
        ('support_maintenance', 'Support & Maintenance'),
        ('other', 'Other Strategic Consultation'),
    )
    TIMELINE_CHOICES = (
        ('immediate', 'Immediate (Within 30 Days)'),
        ('1_to_3_months', '1 - 3 Months'),
        ('3_to_6_months', '3 - 6 Months'),
        ('planning', 'Exploring / Planning Phase'),
    )
    BUDGET_CHOICES = (
        ('under_5k', 'Under $5,000 / ₦5,000,000'),
        ('5k_to_15k', '$5,000 - $15,000'),
        ('15k_to_50k', '$15,000 - $50,000'),
        ('50k_plus', '$50,000+'),
        ('custom', 'To Be Defined / Grant Funded'),
    )
    client_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone_or_whatsapp = models.CharField(max_length=50)
    country = models.CharField(max_length=100, default='Nigeria')
    service_required = models.CharField(max_length=40, choices=SERVICE_CHOICES, default='custom_software')
    project_description = models.TextField()
    desired_timeline = models.CharField(max_length=30, choices=TIMELINE_CHOICES, default='1_to_3_months')
    budget_range = models.CharField(max_length=30, choices=BUDGET_CHOICES, default='5k_to_15k')
    current_system_details = models.TextField(blank=True)
    brief_attachment_url = models.URLField(max_length=500, blank=True)
    privacy_consent_recorded = models.BooleanField(default=True)
    
    # Internal routing
    is_reviewed = models.BooleanField(default=False)
    internal_notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Project inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Project Inquiry: {self.client_name} ({self.organization or 'Individual'})"


class TrainingInquiry(models.Model):
    """
    Novatrix individual or corporate training inquiry submissions.
    """
    TYPE_CHOICES = (
        ('individual', 'Individual Learner'),
        ('corporate', 'Corporate / Institutional Cohort'),
    )
    inquirer_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='individual')
    inquirer_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone_or_whatsapp = models.CharField(max_length=50)
    course = models.ForeignKey(TrainingCourse, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    training_topic_custom = models.CharField(max_length=200, blank=True)
    participant_count = models.PositiveIntegerField(default=1)
    desired_outcome = models.TextField()
    preferred_format = models.CharField(max_length=30, default='live_online')
    target_start_date = models.DateField(null=True, blank=True)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Training inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Training Lead: {self.inquirer_name} ({self.get_inquirer_type_display()})"


class SupportTicket(models.Model):
    """
    Novatrix client maintenance and technical support intake.
    """
    SERVICE_TYPE_CHOICES = (
        ('maintenance', 'Routine Maintenance & Health Checks'),
        ('bug_incident', 'Bug / System Outage'),
        ('enhancement', 'Feature Enhancement / Expansion'),
        ('optimization', 'Performance & Security Optimization'),
    )
    URGENCY_CHOICES = (
        ('low', 'Low - General Question'),
        ('medium', 'Medium - Minor Issue / Non-Blocking'),
        ('high', 'High - Core Feature Degraded'),
        ('critical', 'Critical - Complete Outage / Emergency'),
    )
    STATUS_CHOICES = (
        ('new', 'New Request'),
        ('in_progress', 'Under Investigation / In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    ticket_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    client_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES, default='bug_incident')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    affected_system = models.CharField(max_length=200, help_text="e.g. TIIPE Web Portal, Client ERP")
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket #{self.ticket_number[:8]}: {self.organization} - {self.affected_system}"


class CapabilityDownload(models.Model):
    """
    Brochures, capability statements, and corporate briefs.
    """
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=100, default='Corporate Capability Statement')
    file_url = models.URLField(max_length=500)
    file_size_kb = models.PositiveIntegerField(default=500)
    download_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
