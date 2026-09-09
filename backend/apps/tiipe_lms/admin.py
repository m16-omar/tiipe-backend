from django.contrib import admin
from .models import (
    Program, MentorApplication, MentorAvailability,
    MentorshipSession, LearningModule, Lesson,
    LearnerProgress, PublicHealthResource, PolicyBrief
)

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(MentorApplication)
class MentorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'highest_qualification', 'weekly_availability_hours', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'areas_of_expertise')


@admin.register(MentorAvailability)
class MentorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ('learner', 'mentor', 'subject_topic', 'start_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('learner__email', 'mentor__email', 'subject_topic')


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'level', 'estimated_hours', 'is_published')
    list_filter = ('level', 'is_published', 'program')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]


@admin.register(LearnerProgress)
class LearnerProgressAdmin(admin.ModelAdmin):
    list_display = ('learner', 'module', 'is_completed', 'last_accessed')
    list_filter = ('is_completed',)


@admin.register(PublicHealthResource)
class PublicHealthResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_group', 'download_count', 'published_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'target_group')


@admin.register(PolicyBrief)
class PolicyBriefAdmin(admin.ModelAdmin):
    list_display = ('title', 'research_area', 'authors', 'published_date', 'download_count')
    list_filter = ('research_area',)
    search_fields = ('title', 'abstract', 'authors')
    prepopulated_fields = {'slug': ('title',)}
