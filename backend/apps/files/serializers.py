from rest_framework import serializers
from .models import MediaAsset, DocumentUpload

class MediaAssetSerializer(serializers.ModelSerializer):
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    uploaded_by_email = serializers.ReadOnlyField(source='uploaded_by.email')

    class Meta:
        model = MediaAsset
        fields = '__all__'
        read_only_fields = ('file_size_bytes', 'uploaded_by', 'created_at')


class DocumentUploadSerializer(serializers.ModelSerializer):
    access_display = serializers.CharField(source='get_access_level_display', read_only=True)

    class Meta:
        model = DocumentUpload
        fields = '__all__'
        read_only_fields = ('download_count', 'created_at')
