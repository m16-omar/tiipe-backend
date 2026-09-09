from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HeroSectionViewSet, NavigationMenuViewSet, GovernanceDocumentViewSet,
    BoardMemberViewSet, MediaBroadcastViewSet, WebinarViewSet,
    ImpactMetricViewSet, PublicBenefitStatementViewSet, ArticleCategoryViewSet,
    ArticleViewSet, FAQViewSet, TestimonialViewSet, ContactMessageViewSet,
    EventNoticeViewSet
)

router = DefaultRouter()
router.register(r'heroes', HeroSectionViewSet, basename='cms-heroes')
router.register(r'navigation', NavigationMenuViewSet, basename='cms-navigation')
router.register(r'governance-documents', GovernanceDocumentViewSet, basename='cms-governance')
router.register(r'board-members', BoardMemberViewSet, basename='cms-board-members')
router.register(r'media-broadcasts', MediaBroadcastViewSet, basename='cms-media-broadcasts')
router.register(r'webinars', WebinarViewSet, basename='cms-webinars')
router.register(r'impact-metrics', ImpactMetricViewSet, basename='cms-impact-metrics')
router.register(r'benefit-statements', PublicBenefitStatementViewSet, basename='cms-benefit-statements')
router.register(r'categories', ArticleCategoryViewSet, basename='cms-categories')
router.register(r'articles', ArticleViewSet, basename='cms-articles')
router.register(r'faqs', FAQViewSet, basename='cms-faqs')
router.register(r'testimonials', TestimonialViewSet, basename='cms-testimonials')
router.register(r'contact', ContactMessageViewSet, basename='cms-contact')
router.register(r'events', EventNoticeViewSet, basename='cms-events')

urlpatterns = [
    path('', include(router.urls)),
]
