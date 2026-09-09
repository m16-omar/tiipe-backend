from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, UserProfile, TenantMembership
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    TenantMembershipSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer
)
from apps.core.permissions import IsOwner, IsTenantAdmin

class RegisterView(generics.CreateAPIView):
    """
    Public registration endpoint. Creates user, profile, and links them to current tenant.
    Returns user details along with JWT Access and Refresh tokens.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        user_data = CustomUserSerializer(user, context={'request': request}).data
        
        return Response({
            'success': True,
            'message': 'Account successfully created.',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': user_data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    User login endpoint with email and password.
    Returns JWT tokens and user context including tenant memberships.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        user_data = CustomUserSerializer(user, context={'request': request}).data
        current_tenant = getattr(request, 'tenant', None)
        
        return Response({
            'success': True,
            'message': 'Login successful.',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'active_tenant': {
                'name': current_tenant.name if current_tenant else 'Public',
                'schema': current_tenant.schema_name if current_tenant else 'public',
                'brand': getattr(current_tenant, 'brand_type', 'none')
            },
            'user': user_data
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    Retrieve and update the currently authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user, context={'request': request})
        return Response({'success': True, 'user': serializer.data})

    def patch(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            profile = UserProfile.objects.create(user=request.user)
            
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_serializer = CustomUserSerializer(request.user, context={'request': request})
        return Response({
            'success': True,
            'message': 'Profile updated successfully.',
            'user': user_serializer.data
        })


class ChangePasswordView(APIView):
    """
    Allow authenticated users to change their password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'success': False, 'message': 'Incorrect current password.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'success': True, 'message': 'Password changed successfully.'})


class TenantMembershipViewSet(viewsets.ModelViewSet):
    """
    Manage user roles across tenants.
    """
    serializer_class = TenantMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return TenantMembership.objects.all()
        return TenantMembership.objects.filter(user=user)
