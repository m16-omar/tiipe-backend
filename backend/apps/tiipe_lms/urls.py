from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewSet, MentorApplicationViewSet, MentorAvailabilityViewSet,
    MentorshipSessionViewSet, LearningModuleViewSet, LessonViewSet,
    LearnerProgressViewSet, PublicHealthResourceViewSet, PolicyBriefViewSet
)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='lms-programs')
router.register(r'mentor-applications', MentorApplicationViewSet, basename='lms-mentor-applications')
router.register(r'availabilities', MentorAvailabilityViewSet, basename='lms-availabilities')
router.register(r'sessions', MentorshipSessionViewSet, basename='lms-sessions')
router.register(r'modules', LearningModuleViewSet, basename='lms-modules')
router.register(r'lessons', LessonViewSet, basename='lms-lessons')
router.register(r'progress', LearnerProgressViewSet, basename='lms-progress')
router.register(r'health-resources', PublicHealthResourceViewSet, basename='lms-health-resources')
router.register(r'policy-briefs', PolicyBriefViewSet, basename='lms-policy-briefs')

urlpatterns = [
    path('', include(router.urls)),
]
