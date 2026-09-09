from rest_framework import permissions

class IsTenantAdmin(permissions.BasePermission):
    """
    Allows access only to tenant-level administrators or global superusers.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Check tenant membership role if tenant exists on request
        tenant = getattr(request, 'tenant', None)
        if tenant:
            membership = request.user.tenant_memberships.filter(
                tenant=tenant,
                role='admin',
                is_active=True
            ).exists()
            return membership
        return False


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to allow owners of an object to access/edit it.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Direct user field
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # Learner or mentor ownership
        if hasattr(obj, 'learner') and obj.learner == request.user:
            return True
        if hasattr(obj, 'mentor') and obj.mentor == request.user:
            return True
        
        return False


class IsMentor(permissions.BasePermission):
    """
    Allows access to verified mentors in the current tenant.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        
        tenant = getattr(request, 'tenant', None)
        return request.user.tenant_memberships.filter(
            tenant=tenant,
            role='mentor',
            is_active=True
        ).exists()


class IsLearner(permissions.BasePermission):
    """
    Allows access to registered learners in the current tenant.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        
        tenant = getattr(request, 'tenant', None)
        return request.user.tenant_memberships.filter(
            tenant=tenant,
            role='learner',
            is_active=True
        ).exists()


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Allows read access to any request, but write access only to authenticated staff/admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))
