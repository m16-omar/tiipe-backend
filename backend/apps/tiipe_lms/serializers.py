from rest_framework import serializers
from .models import (
    Program, MentorApplication, MentorAvailability,
    MentorshipSession, LearningModule, Lesson,
    LearnerProgress, PublicHealthResource, PolicyBrief
)
from apps.users.serializers import CustomUserSerializer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LearningModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = LearningModule
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    modules = LearningModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = '__all__'


class MentorApplicationSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = MentorApplication
        fields = '__all__'
        read_only_fields = ('status', 'admin_review_notes', 'reviewed_at', 'created_at')


class MentorAvailabilitySerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    mentor_name = serializers.ReadOnlyField(source='mentor.profile.first_name')

    class Meta:
        model = MentorAvailability
        fields = '__all__'


class MentorshipSessionSerializer(serializers.ModelSerializer):
    learner_details = CustomUserSerializer(source='learner', read_only=True)
    mentor_details = CustomUserSerializer(source='mentor', read_only=True)
    program_title = serializers.ReadOnlyField(source='program.title')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = MentorshipSession
        fields = '__all__'
        read_only_fields = ('created_at',)


class LearnerProgressSerializer(serializers.ModelSerializer):
    module_title = serializers.ReadOnlyField(source='module.title')

    class Meta:
        model = LearnerProgress
        fields = '__all__'
        read_only_fields = ('learner', 'completion_date', 'last_accessed')


class PublicHealthResourceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = PublicHealthResource
        fields = '__all__'


class PolicyBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyBrief
        fields = '__all__'
