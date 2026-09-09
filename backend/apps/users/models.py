from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from apps.core.models import ClientTenant

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is required')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Global Shared User Model across all tenants (TIIPE & Novatrix).
    Enables single sign-on across platforms with role-based tenant memberships.
    """
    email = models.EmailField('email address', unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    Extended profile for a user containing biographical, contact, and compliance data.
    """
    BACKGROUND_CHECK_CHOICES = (
        ('not_applicable', 'Not Applicable'),
        ('pending', 'Pending Verification'),
        ('verified', 'Verified / Cleared'),
        ('rejected', 'Rejected / Ineligible'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True, help_text="Short bio or background summary")
    avatar_url = models.URLField(max_length=500, blank=True)
    
    # Compliance & Mentorship fields (TIIPE / COPPA / Checkr compliance)
    background_check_status = models.CharField(
        max_length=30,
        choices=BACKGROUND_CHECK_CHOICES,
        default='not_applicable'
    )
    background_check_date = models.DateTimeField(null=True, blank=True)
    is_minor = models.BooleanField(default=False, help_text="COPPA compliance flag for youth under 18")
    parental_consent_verified = models.BooleanField(default=False)
    
    # Location
    country = models.CharField(max_length=100, blank=True, default='United States')
    state_or_city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.user.email


class TenantMembership(models.Model):
    """
    Maps a user to a tenant with specific roles and permissions.
    A user can be a Learner in TIIPE, a Training Participant in Novatrix, or an Admin in both.
    """
    ROLE_CHOICES = (
        ('admin', 'Tenant Administrator'),
        ('staff', 'Tenant Staff / Editor'),
        ('mentor', 'TIIPE Verified Mentor / Volunteer'),
        ('learner', 'TIIPE Learner / Student'),
        ('donor', 'TIIPE Donor / Supporter'),
        ('community_partner', 'Community Partner / School'),
        ('client_lead', 'Novatrix Client / Decision-Maker'),
        ('training_student', 'Novatrix Training Participant'),
        ('corporate_buyer', 'Novatrix Corporate Training Buyer'),
        ('support_client', 'Novatrix Support Client'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tenant_memberships')
    tenant = models.ForeignKey(ClientTenant, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='learner')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'tenant', 'role')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.email} - {self.tenant.name} [{self.get_role_display()}]"
