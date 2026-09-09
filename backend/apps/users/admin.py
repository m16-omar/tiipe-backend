from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, TenantMembership

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class TenantMembershipInline(admin.TabularInline):
    model = TenantMembership
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_email_verified', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_email_verified')
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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'background_check_status', 'is_minor')
    list_filter = ('background_check_status', 'is_minor')
    search_fields = ('user__email', 'first_name', 'last_name', 'phone')


@admin.register(TenantMembership)
class TenantMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'role', 'is_active', 'joined_at')
    list_filter = ('tenant', 'role', 'is_active')
    search_fields = ('user__email', 'tenant__name')
