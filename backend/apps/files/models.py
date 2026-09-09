import os
from django.db import models
from django.conf import settings
from django.db import connection

def get_tenant_upload_path(instance, filename):
    schema_name = getattr(connection, 'schema_name', 'public')
    return f"{schema_name}/uploads/{filename}"

class MediaAsset(models.Model):
    """
    Uploaded media assets (images, audio, video, documents) with tenant schema pathing.
    """
    TYPE_CHOICES = (
        ('image', 'Image File (PNG, JPG, WebP, SVG)'),
        ('audio', 'Audio File (MP3, WAV, AAC)'),
        ('video', 'Video File (MP4, WebM)'),
        ('document', 'PDF Document / Worksheet'),
        ('other', 'Other Media Asset'),
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_tenant_upload_path)
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='image')
    file_size_bytes = models.BigIntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_file_type_display()})"

    def save(self, *args, **kwargs):
        if self.file and hasattr(self.file, 'size'):
            self.file_size_bytes = self.file.size
        super().save(*args, **kwargs)


class DocumentUpload(models.Model):
    """
    Downloadable materials (Capability statements, bylaws, student worksheets).
    """
    ACCESS_CHOICES = (
        ('public', 'Public - All Visitors'),
        ('mentor_only', 'Verified Mentors Only'),
        ('learner_only', 'Registered Learners Only'),
        ('client_only', 'Client Accounts Only'),
        ('admin_only', 'Administrators Only'),
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_tenant_upload_path)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20, default='1.0')
    access_level = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='public')
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} v{self.version} [{self.get_access_level_display()}]"
