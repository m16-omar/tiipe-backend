from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    ServicePillar, IndustrySolution, ProjectCaseStudy,
    TrainingCourse, TrainingCohort, ProjectInquiry,
    TrainingInquiry, SupportTicket, CapabilityDownload
)
from .serializers import (
    ServicePillarSerializer, IndustrySolutionSerializer, ProjectCaseStudySerializer,
    TrainingCourseSerializer, TrainingCohortSerializer, ProjectInquirySerializer,
    TrainingInquirySerializer, SupportTicketSerializer, CapabilityDownloadSerializer
)
from apps.core.permissions import IsTenantAdmin

class ServicePillarViewSet(viewsets.ModelViewSet):
    queryset = ServicePillar.objects.filter(is_active=True)
    serializer_class = ServicePillarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class IndustrySolutionViewSet(viewsets.ModelViewSet):
    queryset = IndustrySolution.objects.all()
    serializer_class = IndustrySolutionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class ProjectCaseStudyViewSet(viewsets.ModelViewSet):
    queryset = ProjectCaseStudy.objects.all()
    serializer_class = ProjectCaseStudySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'is_featured', 'industry']
    search_fields = ['title', 'challenge', 'approach', 'solution', 'client_name']
    lookup_field = 'slug'


class TrainingCourseViewSet(viewsets.ModelViewSet):
    queryset = TrainingCourse.objects.filter(is_enrollment_open=True)
    serializer_class = TrainingCourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['topic_category', 'level', 'format']
    search_fields = ['title', 'summary', 'target_audience']
    ordering_fields = ['price_amount', 'duration_weeks']
    lookup_field = 'slug'


class TrainingCohortViewSet(viewsets.ModelViewSet):
    queryset = TrainingCohort.objects.filter(is_registration_active=True)
    serializer_class = TrainingCohortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']


class ProjectInquiryViewSet(viewsets.ModelViewSet):
    queryset = ProjectInquiry.objects.all()
    serializer_class = ProjectInquirySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_required', 'is_reviewed', 'desired_timeline']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsTenantAdmin()]


class TrainingInquiryViewSet(viewsets.ModelViewSet):
    queryset = TrainingInquiry.objects.all()
    serializer_class = TrainingInquirySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['inquirer_type', 'is_reviewed', 'course']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsTenantAdmin()]


class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'urgency', 'service_type']
    search_fields = ['ticket_number', 'client_name', 'organization', 'affected_system']
    ordering_fields = ['created_at', 'urgency']
    lookup_field = 'ticket_number'

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsTenantAdmin()]


class CapabilityDownloadViewSet(viewsets.ModelViewSet):
    queryset = CapabilityDownload.objects.filter(is_active=True)
    serializer_class = CapabilityDownloadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def record_download(self, request, pk=None):
        doc = self.get_object()
        doc.download_count += 1
        doc.save(update_fields=['download_count'])
        return Response({'success': True, 'download_count': doc.download_count, 'file_url': doc.file_url})
