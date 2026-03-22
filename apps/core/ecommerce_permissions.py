from rest_framework.permissions import BasePermission


class IsAdminOrStaffPermission(BasePermission):
    def has_permission(self, request, view):
    #     # Check if the user is authenticated
    #     if request.user.is_authenticated:
    #         # Check if the user is an admin or staff member
    #         return request.user.is_admin or request.user.is_staff
    #     return False
    
        return True

    def has_object_permission(self, request, view, obj):
        # This can be used for object-specific permissions, if needed
        # For example, you can restrict access to specific objects based on user roles.
        return True  # Default to allowing object access
    
class IsOwnerAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False