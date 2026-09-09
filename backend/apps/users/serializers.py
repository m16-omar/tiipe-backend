from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, UserProfile, TenantMembership
from apps.core.models import ClientTenant

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id', 'first_name', 'last_name', 'phone', 'bio', 'avatar_url',
            'background_check_status', 'background_check_date', 'is_minor',
            'parental_consent_verified', 'country', 'state_or_city', 'address',
            'created_at', 'updated_at'
        )
        read_only_fields = ('background_check_status', 'background_check_date', 'parental_consent_verified')


class TenantMembershipSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    tenant_schema = serializers.ReadOnlyField(source='tenant.schema_name')
    brand_type = serializers.ReadOnlyField(source='tenant.brand_type')

    class Meta:
        model = TenantMembership
        fields = ('id', 'tenant', 'tenant_name', 'tenant_schema', 'brand_type', 'role', 'is_active', 'joined_at')


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    tenant_memberships = TenantMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_active', 'is_email_verified', 'is_staff', 'date_joined', 'profile', 'tenant_memberships')


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=TenantMembership.ROLE_CHOICES, default='learner')
    is_minor = serializers.BooleanField(default=False)

    def validate_email(self, value):
        normalized = value.strip().lower()
        if CustomUser.objects.filter(email=normalized).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return normalized

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        phone = validated_data.get('phone', '')
        role = validated_data.get('role', 'learner')
        is_minor = validated_data.get('is_minor', False)

        user = CustomUser.objects.create_user(email=email, password=password)
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_minor=is_minor
        )

        # Attach to current tenant if detected
        request = self.context.get('request')
        tenant = getattr(request, 'tenant', None) if request else None
        if tenant and tenant.schema_name != 'public':
            TenantMembership.objects.create(user=user, tenant=tenant, role=role)
        else:
            # Fallback: assign to default TIIPE tenant if exists
            default_tenant = ClientTenant.objects.filter(brand_type='tiipe').first()
            if default_tenant:
                TenantMembership.objects.create(user=user, tenant=default_tenant, role=role)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is deactivated.')
        else:
            raise serializers.ValidationError('Must include email and password.')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
