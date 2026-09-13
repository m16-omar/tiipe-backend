from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import (
    HeroSection, NavigationMenu, GovernanceDocument, BoardMember,
    MediaBroadcast, Webinar, ImpactMetric, PublicBenefitStatement,
    ArticleCategory, Article, FAQ, Testimonial, ContactMessage, EventNotice
)

@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    list_display = ('page_identifier', 'headline', 'show_active', 'updated_at')
    list_filter = ('is_active',)
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(NavigationMenu)
class NavigationMenuAdmin(ModelAdmin):
    list_display = ('title', 'location', 'show_active')
    list_filter = ('location', 'is_active')
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(GovernanceDocument)
class GovernanceDocumentAdmin(ModelAdmin):
    list_display = ('title', 'show_doc_type', 'published_year', 'download_count', 'show_public')
    list_filter = ('doc_type', 'published_year', 'is_public')
    list_filter_submit = True
    search_fields = ('title', 'description')

    @display(
        description="Type",
        label={
            "bylaws": "info",
            "policy": "warning",
            "tax_exemption": "success",
            "annual_report": "primary",
        }
    )
    def show_doc_type(self, obj):
        return obj.doc_type

    @display(description="Public", boolean=True)
    def show_public(self, obj):
        return obj.is_public


@admin.register(BoardMember)
class BoardMemberAdmin(ModelAdmin):
    list_display = ('name', 'role_title', 'display_order', 'show_active')
    list_filter = ('is_active',)
    list_filter_submit = True
    search_fields = ('name', 'role_title')

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(MediaBroadcast)
class MediaBroadcastAdmin(ModelAdmin):
    list_display = ('title', 'show_type', 'duration_minutes', 'listen_count', 'published_at', 'show_featured')
    list_filter = ('media_type', 'is_featured')
    list_filter_submit = True
    search_fields = ('title', 'summary')

    @display(
        description="Type",
        label={
            "radio": "info",
            "podcast": "warning",
            "interview": "primary",
        }
    )
    def show_type(self, obj):
        return obj.media_type

    @display(description="Featured", boolean=True)
    def show_featured(self, obj):
        return obj.is_featured


@admin.register(Webinar)
class WebinarAdmin(ModelAdmin):
    list_display = ('title', 'host_or_speaker', 'scheduled_start', 'show_completed')
    list_filter = ('is_completed',)
    list_filter_submit = True
    search_fields = ('title', 'host_or_speaker')

    @display(description="Completed", boolean=True)
    def show_completed(self, obj):
        return obj.is_completed


@admin.register(ImpactMetric)
class ImpactMetricAdmin(ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'display_order')


@admin.register(PublicBenefitStatement)
class PublicBenefitStatementAdmin(ModelAdmin):
    list_display = ('title', 'display_order')


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'show_published', 'published_at', 'view_count')
    list_filter = ('is_published', 'category')
    list_filter_submit = True
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}

    @display(description="Published", boolean=True)
    def show_published(self, obj):
        return obj.is_published


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'show_active')
    list_filter = ('category', 'is_active')
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ('author_name', 'author_title', 'rating', 'show_featured')
    list_filter = ('rating', 'is_featured')
    list_filter_submit = True

    @display(description="Featured", boolean=True)
    def show_featured(self, obj):
        return obj.is_featured


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'show_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    list_filter_submit = True
    search_fields = ('full_name', 'email', 'subject', 'message')

    @display(description="Resolved", boolean=True)
    def show_resolved(self, obj):
        return obj.is_resolved


@admin.register(EventNotice)
class EventNoticeAdmin(ModelAdmin):
    list_display = ('title', 'event_type', 'location', 'event_date', 'show_active')
    list_filter = ('event_type', 'is_active')
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active

