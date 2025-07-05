from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Only allows users with role 'super_admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'
