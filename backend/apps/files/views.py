from rest_framework import viewsets, permissions, filters, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import MediaAsset, DocumentUpload
from .serializers import MediaAssetSerializer, DocumentUploadSerializer

class MediaAssetViewSet(viewsets.ModelViewSet):
    queryset = MediaAsset.objects.filter(is_public=True)
    serializer_class = MediaAssetSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['file_type', 'is_public']
    search_fields = ['title', 'alt_text', 'caption']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user if self.request.user.is_authenticated else None)


class DocumentUploadViewSet(viewsets.ModelViewSet):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['access_level']
    search_fields = ['title', 'description']

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def record_download(self, request, pk=None):
        doc = self.get_object()
        doc.download_count += 1
        doc.save(update_fields=['download_count'])
        return Response({'success': True, 'download_count': doc.download_count, 'file_url': doc.file.url if doc.file else ''})
