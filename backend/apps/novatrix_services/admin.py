from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import (
    ServicePillar, IndustrySolution, ProjectCaseStudy,
    TrainingCourse, TrainingCohort, ProjectInquiry,
    TrainingInquiry, SupportTicket, CapabilityDownload
)

class TrainingCohortInline(TabularInline):
    model = TrainingCohort
    extra = 1


@admin.register(ServicePillar)
class ServicePillarAdmin(ModelAdmin):
    list_display = ('title', 'display_order', 'show_active')
    prepopulated_fields = {'slug': ('title',)}
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(IndustrySolution)
class IndustrySolutionAdmin(ModelAdmin):
    list_display = ('name', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectCaseStudy)
class ProjectCaseStudyAdmin(ModelAdmin):
    list_display = ('title', 'client_name', 'show_status', 'show_featured', 'created_at')
    list_filter = ('status', 'is_featured')
    list_filter_submit = True
    search_fields = ('title', 'client_name', 'solution')
    prepopulated_fields = {'slug': ('title',)}

    @display(
        description="Project Status",
        label={
            "delivered": "success",
            "in_development": "warning",
            "concept": "info",
        }
    )
    def show_status(self, obj):
        return obj.status

    @display(description="Featured", boolean=True)
    def show_featured(self, obj):
        return obj.is_featured


@admin.register(TrainingCourse)
class TrainingCourseAdmin(ModelAdmin):
    list_display = ('title', 'topic_category', 'show_level', 'duration_weeks', 'price_amount', 'show_enrolling')
    list_filter = ('topic_category', 'level', 'format', 'is_enrollment_open')
    list_filter_submit = True
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TrainingCohortInline]

    @display(
        description="Skill Level",
        label={
            "beginner": "success",
            "intermediate": "info",
            "advanced": "warning",
        }
    )
    def show_level(self, obj):
        return obj.level

    @display(description="Enrollment Open", boolean=True)
    def show_enrolling(self, obj):
        return obj.is_enrollment_open


@admin.register(TrainingCohort)
class TrainingCohortAdmin(ModelAdmin):
    list_display = ('course', 'cohort_name', 'start_date', 'max_capacity', 'enrolled_count', 'show_registration')
    list_filter = ('is_registration_active', 'start_date')
    list_filter_submit = True

    @display(description="Registration Active", boolean=True)
    def show_registration(self, obj):
        return obj.is_registration_active


@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(ModelAdmin):
    list_display = ('client_name', 'organization', 'service_required', 'desired_timeline', 'budget_range', 'show_reviewed', 'created_at')
    list_filter = ('service_required', 'is_reviewed', 'desired_timeline')
    list_filter_submit = True
    search_fields = ('client_name', 'organization', 'email', 'project_description')

    @display(description="Reviewed", boolean=True)
    def show_reviewed(self, obj):
        return obj.is_reviewed


@admin.register(TrainingInquiry)
class TrainingInquiryAdmin(ModelAdmin):
    list_display = ('inquirer_name', 'show_type', 'course', 'participant_count', 'show_reviewed', 'created_at')
    list_filter = ('inquirer_type', 'is_reviewed')
    list_filter_submit = True
    search_fields = ('inquirer_name', 'organization', 'email')

    @display(
        description="Inquiry Type",
        label={
            "individual": "info",
            "corporate": "warning",
        }
    )
    def show_type(self, obj):
        return obj.inquirer_type

    @display(description="Reviewed", boolean=True)
    def show_reviewed(self, obj):
        return obj.is_reviewed


@admin.register(SupportTicket)
class SupportTicketAdmin(ModelAdmin):
    list_display = ('ticket_number', 'client_name', 'organization', 'service_type', 'show_urgency', 'show_status', 'created_at')
    list_filter = ('status', 'urgency', 'service_type')
    list_filter_submit = True
    search_fields = ('ticket_number', 'organization', 'client_name', 'email', 'issue_description')

    @display(
        description="Urgency",
        label={
            "critical": "danger",
            "high": "warning",
            "medium": "info",
            "low": "secondary",
        }
    )
    def show_urgency(self, obj):
        return obj.urgency

    @display(
        description="Status",
        label={
            "resolved": "success",
            "in_progress": "info",
            "new": "warning",
            "closed": "secondary",
        }
    )
    def show_status(self, obj):
        return obj.status


@admin.register(CapabilityDownload)
class CapabilityDownloadAdmin(ModelAdmin):
    list_display = ('title', 'document_type', 'download_count', 'show_active')
    list_filter = ('document_type', 'is_active')
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active
