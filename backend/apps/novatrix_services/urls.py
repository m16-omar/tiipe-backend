from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServicePillarViewSet, IndustrySolutionViewSet, ProjectCaseStudyViewSet,
    TrainingCourseViewSet, TrainingCohortViewSet, ProjectInquiryViewSet,
    TrainingInquiryViewSet, SupportTicketViewSet, CapabilityDownloadViewSet
)

router = DefaultRouter()
router.register(r'pillars', ServicePillarViewSet, basename='services-pillars')
router.register(r'industries', IndustrySolutionViewSet, basename='services-industries')
router.register(r'case-studies', ProjectCaseStudyViewSet, basename='services-case-studies')
router.register(r'courses', TrainingCourseViewSet, basename='services-courses')
router.register(r'cohorts', TrainingCohortViewSet, basename='services-cohorts')
router.register(r'project-inquiries', ProjectInquiryViewSet, basename='services-project-inquiries')
router.register(r'training-inquiries', TrainingInquiryViewSet, basename='services-training-inquiries')
router.register(r'support-tickets', SupportTicketViewSet, basename='services-support-tickets')
router.register(r'downloads', CapabilityDownloadViewSet, basename='services-downloads')

urlpatterns = [
    path('', include(router.urls)),
]
