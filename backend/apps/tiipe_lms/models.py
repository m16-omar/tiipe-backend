from django.db import models
from django.conf import settings
from django.utils import timezone

class Program(models.Model):
    """
    TIIPE Core Initiatives (Academic Tutoring, Workforce, Public Health, Civic Engagement).
    """
    CATEGORY_CHOICES = (
        ('education_tutoring', 'Academic Tutoring & Mentorship'),
        ('workforce_development', 'Workforce Development & Digital Literacy'),
        ('public_health', 'Public Health Education & Maternal Literacy'),
        ('civic_engagement', 'Civic Engagement & Outreach'),
        ('community_research', 'Community-Based Research'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='education_tutoring')
    summary = models.TextField()
    description = models.TextField()
    impact_goal = models.CharField(max_length=255, blank=True, help_text="e.g. 'Empower 1,000 students in 2026'")
    target_audience = models.CharField(max_length=255, blank=True)
    cover_image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class MentorApplication(models.Model):
    """
    Volunteer and mentor onboarding application with background verification tracking.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved / Verified'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_applications')
    areas_of_expertise = models.CharField(max_length=255, help_text="e.g. Mathematics, Python, Career Guidance")
    highest_qualification = models.CharField(max_length=150)
    current_employer_or_school = models.CharField(max_length=200, blank=True)
    linkedin_or_portfolio = models.URLField(max_length=500, blank=True)
    id_document_url = models.URLField(max_length=500, blank=True, help_text="Secure S3 URL for background check")
    background_check_reference = models.CharField(max_length=100, blank=True, help_text="Checkr API Verification ID")
    weekly_availability_hours = models.PositiveSmallIntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Mentor App: {self.user.email} - {self.get_status_display()}"


class MentorAvailability(models.Model):
    """
    Weekly schedule slots for verified mentors.
    """
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Mentor availabilities'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.mentor.email} - {self.get_day_of_week_display()} ({self.start_time} to {self.end_time})"


class MentorshipSession(models.Model):
    """
    Scheduled 1-on-1 tutoring / mentorship sessions between a Learner and Mentor.
    """
    STATUS_CHOICES = (
        ('requested', 'Session Requested'),
        ('scheduled', 'Confirmed & Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    learner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learner_sessions')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_sessions')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, related_name='sessions')
    subject_topic = models.CharField(max_length=200, help_text="e.g. Algebra 1, Python Functions, Resume Review")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    meeting_link = models.URLField(max_length=500, blank=True, help_text="Jitsi, Zoom or Google Meet URL")
    feedback_notes = models.TextField(blank=True, help_text="Post-session progress notes by mentor")
    learner_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    worksheet_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Session: {self.learner.email} with {self.mentor.email} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class LearningModule(models.Model):
    """
    Micro-learning interactive pathway for digital literacy and workforce skills.
    """
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    estimated_hours = models.PositiveIntegerField(default=4)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"


class Lesson(models.Model):
    """
    Individual lesson / unit inside a LearningModule. Supports offline worksheets.
    """
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0)
    content_body = models.TextField(help_text="Lesson content in markdown")
    video_url = models.URLField(max_length=500, blank=True)
    worksheet_download_url = models.URLField(max_length=500, blank=True, help_text="Offline study PDF worksheet")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.module.title} - Lesson {self.display_order}: {self.title}"


class LearnerProgress(models.Model):
    """
    Tracks learner module completions and certificate eligibility.
    """
    learner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='learner_progress')
    completed_lessons = models.JSONField(default=list, help_text="List of completed lesson IDs")
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    certificate_url = models.URLField(max_length=500, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('learner', 'module')

    def __str__(self):
        return f"Progress: {self.learner.email} in {self.module.title}"


class PublicHealthResource(models.Model):
    """
    TIIPE Public Health Portal: Maternal health literacy, disease prevention pamphlets.
    """
    CATEGORY_CHOICES = (
        ('maternal_health', 'Maternal & Child Health Literacy'),
        ('disease_prevention', 'Chronic Disease & Infection Prevention'),
        ('nutrition_wellness', 'Community Nutrition & Wellness'),
        ('mental_health', 'Mental Health & Resilience'),
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='maternal_health')
    description = models.TextField()
    target_group = models.CharField(max_length=150, blank=True, help_text="e.g. Expecting Mothers, Seniors, Youth")
    file_download_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} [{self.get_category_display()}]"


class PolicyBrief(models.Model):
    """
    TIIPE Open-Access Research Portal: Community-based policy briefs and academic papers.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    abstract = models.TextField()
    authors = models.CharField(max_length=255, default='TIIPE Research Working Group')
    research_area = models.CharField(max_length=150, help_text="e.g. Educational Equity, Health Disparities")
    doi_or_reference = models.CharField(max_length=150, blank=True)
    pdf_download_url = models.URLField(max_length=500)
    citation_text = models.TextField(blank=True)
    download_count = models.PositiveIntegerField(default=0)
    published_date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
