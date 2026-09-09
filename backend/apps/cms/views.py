from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    HeroSection, NavigationMenu, GovernanceDocument, BoardMember,
    MediaBroadcast, Webinar, ImpactMetric, PublicBenefitStatement,
    ArticleCategory, Article, FAQ, Testimonial, ContactMessage, EventNotice
)
from .serializers import (
    HeroSectionSerializer, NavigationMenuSerializer, GovernanceDocumentSerializer,
    BoardMemberSerializer, MediaBroadcastSerializer, WebinarSerializer,
    ImpactMetricSerializer, PublicBenefitStatementSerializer, ArticleCategorySerializer,
    ArticleSerializer, FAQSerializer, TestimonialSerializer, ContactMessageSerializer,
    EventNoticeSerializer
)
from apps.core.permissions import IsTenantAdmin

class HeroSectionViewSet(viewsets.ModelViewSet):
    queryset = HeroSection.objects.filter(is_active=True)
    serializer_class = HeroSectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page_identifier']


class NavigationMenuViewSet(viewsets.ModelViewSet):
    queryset = NavigationMenu.objects.filter(is_active=True)
    serializer_class = NavigationMenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']


class GovernanceDocumentViewSet(viewsets.ModelViewSet):
    queryset = GovernanceDocument.objects.filter(is_public=True)
    serializer_class = GovernanceDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['doc_type', 'published_year']
    search_fields = ['title', 'description']
    ordering_fields = ['published_year', 'download_count', 'created_at']

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def record_download(self, request, pk=None):
        doc = self.get_object()
        doc.download_count += 1
        doc.save(update_fields=['download_count'])
        return Response({'success': True, 'download_count': doc.download_count, 'file_url': doc.file_url})


class BoardMemberViewSet(viewsets.ModelViewSet):
    queryset = BoardMember.objects.filter(is_active=True)
    serializer_class = BoardMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MediaBroadcastViewSet(viewsets.ModelViewSet):
    queryset = MediaBroadcast.objects.all()
    serializer_class = MediaBroadcastSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['media_type', 'is_featured']
    search_fields = ['title', 'summary']

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def record_listen(self, request, pk=None):
        item = self.get_object()
        item.listen_count += 1
        item.save(update_fields=['listen_count'])
        return Response({'success': True, 'listen_count': item.listen_count})


class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_completed']
    ordering_fields = ['scheduled_start']


class ImpactMetricViewSet(viewsets.ModelViewSet):
    queryset = ImpactMetric.objects.all()
    serializer_class = ImpactMetricSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PublicBenefitStatementViewSet(viewsets.ModelViewSet):
    queryset = PublicBenefitStatement.objects.all()
    serializer_class = PublicBenefitStatementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticleCategoryViewSet(viewsets.ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'category']
    search_fields = ['title', 'summary', 'body']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_featured']


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsTenantAdmin()]


class EventNoticeViewSet(viewsets.ModelViewSet):
    queryset = EventNotice.objects.filter(is_active=True)
    serializer_class = EventNoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
