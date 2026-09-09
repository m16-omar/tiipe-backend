from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import (
    Program, MentorApplication, MentorAvailability,
    MentorshipSession, LearningModule, Lesson,
    LearnerProgress, PublicHealthResource, PolicyBrief
)
from .serializers import (
    ProgramSerializer, MentorApplicationSerializer, MentorAvailabilitySerializer,
    MentorshipSessionSerializer, LearningModuleSerializer, LessonSerializer,
    LearnerProgressSerializer, PublicHealthResourceSerializer, PolicyBriefSerializer
)
from apps.core.permissions import IsTenantAdmin, IsMentor, IsLearner, IsOwner

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.filter(is_active=True)
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'summary', 'description']
    lookup_field = 'slug'


class MentorApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = MentorApplicationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return MentorApplication.objects.none()
        if user.is_staff or user.is_superuser:
            return MentorApplication.objects.all()
        return MentorApplication.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsTenantAdmin])
    def approve(self, request, pk=None):
        app = self.get_object()
        app.status = 'approved'
        app.reviewed_at = timezone.now()
        app.admin_review_notes = request.data.get('admin_review_notes', 'Approved by administrator.')
        app.save()

        # Update user profile background check status
        profile = getattr(app.user, 'profile', None)
        if profile:
            profile.background_check_status = 'verified'
            profile.background_check_date = timezone.now()
            profile.save()

        # Assign mentor role in membership
        tenant = getattr(request, 'tenant', None)
        if tenant:
            membership, _ = app.user.tenant_memberships.get_or_create(
                tenant=tenant,
                role='mentor'
            )
            membership.is_active = True
            membership.save()

        return Response({'success': True, 'message': f'Mentor application for {app.user.email} approved.'})


class MentorAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = MentorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['day_of_week', 'is_active']

    def get_queryset(self):
        if self.request.user.is_staff:
            return MentorAvailability.objects.all()
        return MentorAvailability.objects.filter(mentor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


class MentorshipSessionViewSet(viewsets.ModelViewSet):
    serializer_class = MentorshipSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'program']
    ordering_fields = ['start_time', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return MentorshipSession.objects.all()
        return MentorshipSession.objects.filter(learner=user) | MentorshipSession.objects.filter(mentor=user)

    def perform_create(self, serializer):
        # Auto-generate video meeting room link
        import uuid
        room_name = f"tiipe-session-{uuid.uuid4().hex[:10]}"
        meeting_link = f"https://meet.jit.si/{room_name}"
        serializer.save(learner=self.request.user, meeting_link=meeting_link)

    @action(detail=True, methods=['post'])
    def complete_session(self, request, pk=None):
        session = self.get_object()
        if request.user not in (session.mentor, session.learner) and not request.user.is_staff:
            return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        session.status = 'completed'
        if 'feedback_notes' in request.data:
            session.feedback_notes = request.data['feedback_notes']
        if 'learner_rating' in request.data:
            session.learner_rating = request.data['learner_rating']
        session.save()
        return Response({'success': True, 'message': 'Session marked as completed.'})


class LearningModuleViewSet(viewsets.ModelViewSet):
    queryset = LearningModule.objects.filter(is_published=True)
    serializer_class = LearningModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['program', 'level']
    lookup_field = 'slug'


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['module']


class LearnerProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LearnerProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LearnerProgress.objects.filter(learner=self.request.user)

    @action(detail=False, methods=['post'])
    def record_lesson(self, request):
        module_id = request.data.get('module_id')
        lesson_id = request.data.get('lesson_id')
        
        if not module_id or not lesson_id:
            return Response({'error': 'module_id and lesson_id are required'}, status=400)
            
        progress, _ = LearnerProgress.objects.get_or_create(
            learner=request.user,
            module_id=module_id
        )
        if lesson_id not in progress.completed_lessons:
            progress.completed_lessons.append(lesson_id)
            progress.save()
            
        return Response({'success': True, 'completed_lessons': progress.completed_lessons})


class PublicHealthResourceViewSet(viewsets.ModelViewSet):
    queryset = PublicHealthResource.objects.all()
    serializer_class = PublicHealthResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description', 'target_group']

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def record_download(self, request, pk=None):
        resource = self.get_object()
        resource.download_count += 1
        resource.save(update_fields=['download_count'])
        return Response({'success': True, 'download_count': resource.download_count, 'file_url': resource.file_download_url})


class PolicyBriefViewSet(viewsets.ModelViewSet):
    queryset = PolicyBrief.objects.all()
    serializer_class = PolicyBriefSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'abstract', 'authors', 'research_area']
    ordering_fields = ['published_date', 'download_count']
    lookup_field = 'slug'

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def record_download(self, request, slug=None):
        brief = self.get_object()
        brief.download_count += 1
        brief.save(update_fields=['download_count'])
        return Response({'success': True, 'download_count': brief.download_count, 'pdf_url': brief.pdf_download_url})
