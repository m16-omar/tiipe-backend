from django.contrib import admin
from .models import (
    HeroSection, NavigationMenu, GovernanceDocument, BoardMember,
    MediaBroadcast, Webinar, ImpactMetric, PublicBenefitStatement,
    ArticleCategory, Article, FAQ, Testimonial, ContactMessage, EventNotice
)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('page_identifier', 'headline', 'is_active', 'updated_at')
    list_filter = ('is_active',)


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active')
    list_filter = ('location', 'is_active')


@admin.register(GovernanceDocument)
class GovernanceDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'published_year', 'download_count', 'is_public')
    list_filter = ('doc_type', 'published_year', 'is_public')
    search_fields = ('title', 'description')


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_title', 'display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'role_title')


@admin.register(MediaBroadcast)
class MediaBroadcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'duration_minutes', 'listen_count', 'published_at', 'is_featured')
    list_filter = ('media_type', 'is_featured')
    search_fields = ('title', 'summary')


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'host_or_speaker', 'scheduled_start', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('title', 'host_or_speaker')


@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'display_order')


@admin.register(PublicBenefitStatement)
class PublicBenefitStatementAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order')


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'is_published', 'published_at', 'view_count')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'is_active')
    list_filter = ('category', 'is_active')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'rating', 'is_featured')
    list_filter = ('rating', 'is_featured')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')


@admin.register(EventNotice)
class EventNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'location', 'event_date', 'is_active')
    list_filter = ('event_type', 'is_active')
