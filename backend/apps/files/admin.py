from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import MediaAsset, DocumentUpload

@admin.register(MediaAsset)
class MediaAssetAdmin(ModelAdmin):
    list_display = ('title', 'show_type', 'file_size_bytes', 'show_public', 'uploaded_by', 'created_at')
    list_filter = ('file_type', 'is_public')
    list_filter_submit = True
    search_fields = ('title', 'alt_text', 'caption')

    @display(
        description="Type",
        label={
            "image": "success",
            "audio": "info",
            "video": "warning",
            "document": "primary",
        }
    )
    def show_type(self, obj):
        return obj.file_type

    @display(description="Public", boolean=True)
    def show_public(self, obj):
        return obj.is_public


@admin.register(DocumentUpload)
class DocumentUploadAdmin(ModelAdmin):
    list_display = ('title', 'version', 'show_access', 'download_count', 'created_at')
    list_filter = ('access_level',)
    list_filter_submit = True
    search_fields = ('title', 'description')

    @display(
        description="Access Level",
        label={
            "public": "success",
            "members_only": "info",
            "internal_staff": "danger",
        }
    )
    def show_access(self, obj):
        return obj.access_level

