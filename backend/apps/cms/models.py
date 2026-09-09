from django.db import models
from django.utils import timezone

class HeroSection(models.Model):
    """
    Tenant-specific hero section configuration for homepage and primary landing view.
    """
    page_identifier = models.CharField(max_length=50, default='home', help_text="e.g. 'home', 'programs', 'services'")
    headline = models.CharField(max_length=255)
    subheadline = models.TextField()
    cta_primary_text = models.CharField(max_length=100, blank=True)
    cta_primary_link = models.CharField(max_length=255, blank=True)
    cta_secondary_text = models.CharField(max_length=100, blank=True)
    cta_secondary_link = models.CharField(max_length=255, blank=True)
    cta_tertiary_text = models.CharField(max_length=100, blank=True)
    cta_tertiary_link = models.CharField(max_length=255, blank=True)
    background_image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.page_identifier} Hero: {self.headline[:40]}"


class NavigationMenu(models.Model):
    """
    Tenant navigation bar & footer menu structures.
    """
    MENU_LOCATION_CHOICES = (
        ('header', 'Header Primary Navigation'),
        ('footer_quick', 'Footer Quick Links'),
        ('footer_services', 'Footer Services / Programs'),
        ('footer_legal', 'Footer Legal & Governance'),
    )
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=30, choices=MENU_LOCATION_CHOICES, default='header')
    items = models.JSONField(default=list, help_text="List of items: [{'label': 'Home', 'path': '/', 'order': 1}]")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_location_display()} ({self.title})"


class GovernanceDocument(models.Model):
    """
    TIIPE Governance Center Documents (Bylaws, 501(c)(3), Form 990, Conflict of Interest).
    """
    DOC_TYPE_CHOICES = (
        ('bylaws', 'Corporate Bylaws'),
        ('conflict_of_interest', 'Conflict of Interest & Recusal Standards'),
        ('501c3_status', '501(c)(3) IRS Determination Letter'),
        ('form_990', 'Form 990 Tax Return'),
        ('annual_report', 'Annual Impact & Financial Report'),
        ('ethics_charter', 'Code of Ethics & Public Benefit Charter'),
        ('other', 'General Governance Policy'),
    )
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=40, choices=DOC_TYPE_CHOICES, default='bylaws')
    description = models.TextField(blank=True)
    file_url = models.URLField(max_length=500, help_text="S3 / Spaces document URL")
    file_size_bytes = models.BigIntegerField(default=0)
    published_year = models.IntegerField(default=timezone.now().year)
    is_public = models.BooleanField(default=True)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_year', 'doc_type']

    def __str__(self):
        return f"{self.title} ({self.get_doc_type_display()})"


class BoardMember(models.Model):
    """
    TIIPE Board of Directors and Executive Bios.
    """
    name = models.CharField(max_length=150)
    role_title = models.CharField(max_length=150, help_text="e.g. President, Board Chair, Treasurer")
    bio = models.TextField()
    photo_url = models.URLField(max_length=500, blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role_title}"


class MediaBroadcast(models.Model):
    """
    TIIPE Media Hub: AdieTalk Radio, podcasts, and digital broadcasts.
    """
    MEDIA_TYPE_CHOICES = (
        ('adietalk_radio', 'AdieTalk Radio Live/Stream'),
        ('podcast', 'TIIPE Podcast Episode'),
        ('video', 'Video Presentation / Feature'),
        ('interview', 'Community & Expert Interview'),
    )
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=30, choices=MEDIA_TYPE_CHOICES, default='podcast')
    episode_number = models.PositiveIntegerField(null=True, blank=True)
    summary = models.TextField()
    stream_url = models.URLField(max_length=500, help_text="Direct MP3 / Stream link")
    external_embed_url = models.URLField(max_length=500, blank=True, help_text="YouTube, Spotify or SoundCloud embed")
    thumbnail_url = models.URLField(max_length=500, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    listen_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.get_media_type_display()}: {self.title}"


class Webinar(models.Model):
    """
    Upcoming and recorded public health and workforce webinars.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    host_or_speaker = models.CharField(max_length=255)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    registration_link = models.URLField(max_length=500, blank=True)
    meeting_link = models.URLField(max_length=500, blank=True)
    recording_url = models.URLField(max_length=500, blank=True)
    is_completed = models.BooleanField(default=False)
    attendee_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-scheduled_start']

    def __str__(self):
        return self.title


class ImpactMetric(models.Model):
    """
    Counters displaying key metrics (e.g. 500+ Students Mentored, $100K Raised).
    """
    label = models.CharField(max_length=150)
    value = models.CharField(max_length=50, help_text="e.g. '500', '10,000', '100%'")
    suffix = models.CharField(max_length=20, blank=True, help_text="e.g. '+', 'K', '%'")
    description = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class PublicBenefitStatement(models.Model):
    """
    Empowerment, Inclusiveness, and Transparency statements / brand values.
    """
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_name = models.CharField(max_length=100, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Insights, Articles, Announcements, and Research news.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, related_name='articles')
    summary = models.TextField()
    body = models.TextField(help_text="Markdown or HTML formatted article content")
    author_name = models.CharField(max_length=150, default='Editorial Team')
    featured_image_url = models.URLField(max_length=500, blank=True)
    read_time_minutes = models.PositiveIntegerField(default=5)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO Fields
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, default='General')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    author_name = models.CharField(max_length=150)
    author_title = models.CharField(max_length=150, blank=True)
    author_organization = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.author_name} - {self.quote[:30]}"


class ContactMessage(models.Model):
    """
    General contact inquiry messages submitted on the tenant website.
    """
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.full_name}: {self.subject}"


class EventNotice(models.Model):
    """
    Community Events and Announcement Listings [Found on live website - NEEDS CONFIRMATION].
    """
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100, default='Community Gathering')
    location = models.CharField(max_length=255, default='Online / New Rochelle, NY')
    event_date = models.DateTimeField()
    description = models.TextField()
    registration_url = models.URLField(max_length=500, blank=True)
    banner_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} ({self.event_date.strftime('%Y-%m-%d')})"
