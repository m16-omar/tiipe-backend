from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import display
from .models import (
    Program, MentorApplication, MentorAvailability,
    MentorshipSession, LearningModule, Lesson,
    LearnerProgress, PublicHealthResource, PolicyBrief
)

class LessonInline(StackedInline):
    model = Lesson
    extra = 1


@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ('title', 'show_category', 'show_active', 'created_at')
    list_filter = ('category', 'is_active')
    list_filter_submit = True
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    @display(
        description="Category",
        label={
            "education": "info",
            "health": "success",
            "civic": "warning",
            "partnership": "primary",
        }
    )
    def show_category(self, obj):
        return obj.category

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(MentorApplication)
class MentorApplicationAdmin(ModelAdmin):
    list_display = ('user', 'highest_qualification', 'weekly_availability_hours', 'show_status', 'created_at')
    list_filter = ('status',)
    list_filter_submit = True
    search_fields = ('user__email', 'areas_of_expertise')

    @display(
        description="Application Status",
        label={
            "approved": "success",
            "pending": "warning",
            "rejected": "danger",
            "under_review": "info",
        }
    )
    def show_status(self, obj):
        return obj.status


@admin.register(MentorAvailability)
class MentorAvailabilityAdmin(ModelAdmin):
    list_display = ('mentor', 'day_of_week', 'start_time', 'end_time', 'show_active')
    list_filter = ('day_of_week', 'is_active')
    list_filter_submit = True

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(ModelAdmin):
    list_display = ('learner', 'mentor', 'subject_topic', 'start_time', 'show_status')
    list_filter = ('status', 'start_time')
    list_filter_submit = True
    search_fields = ('learner__email', 'mentor__email', 'subject_topic')

    @display(
        description="Status",
        label={
            "completed": "success",
            "scheduled": "info",
            "requested": "warning",
            "cancelled": "danger",
        }
    )
    def show_status(self, obj):
        return obj.status


@admin.register(LearningModule)
class LearningModuleAdmin(ModelAdmin):
    list_display = ('title', 'program', 'show_level', 'estimated_hours', 'show_published')
    list_filter = ('level', 'is_published', 'program')
    list_filter_submit = True
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]

    @display(
        description="Level",
        label={
            "beginner": "success",
            "intermediate": "info",
            "advanced": "warning",
        }
    )
    def show_level(self, obj):
        return obj.level

    @display(description="Published", boolean=True)
    def show_published(self, obj):
        return obj.is_published


@admin.register(LearnerProgress)
class LearnerProgressAdmin(ModelAdmin):
    list_display = ('learner', 'module', 'show_completed', 'last_accessed')
    list_filter = ('is_completed',)
    list_filter_submit = True

    @display(description="Completed", boolean=True)
    def show_completed(self, obj):
        return obj.is_completed


@admin.register(PublicHealthResource)
class PublicHealthResourceAdmin(ModelAdmin):
    list_display = ('title', 'category', 'target_group', 'download_count', 'published_at')
    list_filter = ('category',)
    list_filter_submit = True
    search_fields = ('title', 'description', 'target_group')


@admin.register(PolicyBrief)
class PolicyBriefAdmin(ModelAdmin):
    list_display = ('title', 'research_area', 'authors', 'published_date', 'download_count')
    list_filter = ('research_area',)
    list_filter_submit = True
    search_fields = ('title', 'abstract', 'authors')
    prepopulated_fields = {'slug': ('title',)}

