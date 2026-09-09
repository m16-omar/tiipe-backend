from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaAssetViewSet, DocumentUploadViewSet

router = DefaultRouter()
router.register(r'assets', MediaAssetViewSet, basename='files-assets')
router.register(r'documents', DocumentUploadViewSet, basename='files-documents')

urlpatterns = [
    path('', include(router.urls)),
]
