from rest_framework import serializers
from .models import (
    ServicePillar, IndustrySolution, ProjectCaseStudy,
    TrainingCourse, TrainingCohort, ProjectInquiry,
    TrainingInquiry, SupportTicket, CapabilityDownload
)

class ServicePillarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePillar
        fields = '__all__'


class IndustrySolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrySolution
        fields = '__all__'


class ProjectCaseStudySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ProjectCaseStudy
        fields = '__all__'


class TrainingCohortSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = TrainingCohort
        fields = '__all__'


class TrainingCourseSerializer(serializers.ModelSerializer):
    cohorts = TrainingCohortSerializer(many=True, read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    topic_display = serializers.CharField(source='get_topic_category_display', read_only=True)

    class Meta:
        model = TrainingCourse
        fields = '__all__'


class ProjectInquirySerializer(serializers.ModelSerializer):
    service_display = serializers.CharField(source='get_service_required_display', read_only=True)
    timeline_display = serializers.CharField(source='get_desired_timeline_display', read_only=True)
    budget_display = serializers.CharField(source='get_budget_range_display', read_only=True)

    class Meta:
        model = ProjectInquiry
        fields = '__all__'
        read_only_fields = ('is_reviewed', 'internal_notes', 'assigned_to', 'created_at')


class TrainingInquirySerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    inquirer_type_display = serializers.CharField(source='get_inquirer_type_display', read_only=True)

    class Meta:
        model = TrainingInquiry
        fields = '__all__'
        read_only_fields = ('is_reviewed', 'created_at')


class SupportTicketSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SupportTicket
        fields = '__all__'
        read_only_fields = ('ticket_number', 'status', 'resolution_notes', 'created_at', 'updated_at')


class CapabilityDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapabilityDownload
        fields = '__all__'
