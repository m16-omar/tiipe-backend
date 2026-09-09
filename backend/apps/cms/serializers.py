from rest_framework import serializers
from .models import (
    HeroSection, NavigationMenu, GovernanceDocument, BoardMember,
    MediaBroadcast, Webinar, ImpactMetric, PublicBenefitStatement,
    ArticleCategory, Article, FAQ, Testimonial, ContactMessage, EventNotice
)

class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'


class NavigationMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationMenu
        fields = '__all__'


class GovernanceDocumentSerializer(serializers.ModelSerializer):
    doc_type_display = serializers.CharField(source='get_doc_type_display', read_only=True)

    class Meta:
        model = GovernanceDocument
        fields = '__all__'


class BoardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = '__all__'


class MediaBroadcastSerializer(serializers.ModelSerializer):
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)

    class Meta:
        model = MediaBroadcast
        fields = '__all__'


class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = '__all__'


class ImpactMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactMetric
        fields = '__all__'


class PublicBenefitStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicBenefitStatement
        fields = '__all__'


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('is_resolved', 'created_at')


class EventNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNotice
        fields = '__all__'
