from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display
from .models import CustomUser, UserProfile, TenantMembership

class UserProfileInline(StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class TenantMembershipInline(TabularInline):
    model = TenantMembership
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'show_staff', 'show_active', 'show_verified', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_email_verified')
    list_filter_submit = True
    ordering = ('-date_joined',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    inlines = (UserProfileInline, TenantMembershipInline)

    @display(description="Staff", boolean=True)
    def show_staff(self, obj):
        return obj.is_staff

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active

    @display(description="Verified", boolean=True)
    def show_verified(self, obj):
        return obj.is_email_verified


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'show_bg_check', 'show_minor')
    list_filter = ('background_check_status', 'is_minor')
    list_filter_submit = True
    search_fields = ('user__email', 'first_name', 'last_name', 'phone')

    @display(
        description="Background Check",
        label={
            "verified": "success",
            "pending": "warning",
            "rejected": "danger",
            "not_submitted": "secondary",
        }
    )
    def show_bg_check(self, obj):
        return obj.background_check_status

    @display(description="Minor (<18)", boolean=True)
    def show_minor(self, obj):
        return obj.is_minor


@admin.register(TenantMembership)
class TenantMembershipAdmin(ModelAdmin):
    list_display = ('user', 'tenant', 'show_role', 'show_active', 'joined_at')
    list_filter = ('tenant', 'role', 'is_active')
    list_filter_submit = True
    search_fields = ('user__email', 'tenant__name')

    @display(
        description="Role",
        label={
            "admin": "danger",
            "mentor": "info",
            "learner": "success",
            "partner": "warning",
            "donor": "primary",
        }
    )
    def show_role(self, obj):
        return obj.role

    @display(description="Active", boolean=True)
    def show_active(self, obj):
        return obj.is_active

