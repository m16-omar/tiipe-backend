from django.contrib import admin
from .models import (
    ServicePillar, IndustrySolution, ProjectCaseStudy,
    TrainingCourse, TrainingCohort, ProjectInquiry,
    TrainingInquiry, SupportTicket, CapabilityDownload
)

class TrainingCohortInline(admin.TabularInline):
    model = TrainingCohort
    extra = 1


@admin.register(ServicePillar)
class ServicePillarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(IndustrySolution)
class IndustrySolutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectCaseStudy)
class ProjectCaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured')
    search_fields = ('title', 'client_name', 'solution')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic_category', 'level', 'format', 'duration_weeks', 'price_amount', 'is_enrollment_open')
    list_filter = ('topic_category', 'level', 'format', 'is_enrollment_open')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TrainingCohortInline]


@admin.register(TrainingCohort)
class TrainingCohortAdmin(admin.ModelAdmin):
    list_display = ('course', 'cohort_name', 'start_date', 'max_capacity', 'enrolled_count', 'is_registration_active')
    list_filter = ('is_registration_active', 'start_date')


@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'organization', 'service_required', 'desired_timeline', 'budget_range', 'is_reviewed', 'created_at')
    list_filter = ('service_required', 'is_reviewed', 'desired_timeline')
    search_fields = ('client_name', 'organization', 'email', 'project_description')


@admin.register(TrainingInquiry)
class TrainingInquiryAdmin(admin.ModelAdmin):
    list_display = ('inquirer_name', 'inquirer_type', 'course', 'participant_count', 'is_reviewed', 'created_at')
    list_filter = ('inquirer_type', 'is_reviewed')
    search_fields = ('inquirer_name', 'organization', 'email')


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'organization', 'service_type', 'urgency', 'status', 'created_at')
    list_filter = ('status', 'urgency', 'service_type')
    search_fields = ('ticket_number', 'organization', 'client_name', 'issue_description')


@admin.register(CapabilityDownload)
class CapabilityDownloadAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'download_count', 'is_active')
