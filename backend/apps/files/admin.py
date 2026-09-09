from django.contrib import admin
from .models import MediaAsset, DocumentUpload

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'file_size_bytes', 'is_public', 'uploaded_by', 'created_at')
    list_filter = ('file_type', 'is_public')
    search_fields = ('title', 'alt_text', 'caption')


@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'access_level', 'download_count', 'created_at')
    list_filter = ('access_level',)
    search_fields = ('title', 'description')
