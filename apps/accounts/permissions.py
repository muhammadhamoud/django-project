from rest_framework.permissions import BasePermission
from properties.models import Property


class HasPermission(BasePermission):
    """
    Generic RBAC permission checker
    """

    def __init__(self, permission_code=None):
        self.permission_code = permission_code

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        # Admin bypass
        if request.user.is_superuser or request.user.is_admin:
            return True

        profile = getattr(request.user, "profile", None)

        if not profile:
            return False

        if not self.permission_code:
            return True

        return profile.has_permission(self.permission_code)


# 🔥 Factory function (THIS is what you import)
def permission_required(code):
    class CustomPermission(HasPermission):
        def __init__(self):
            super().__init__(code)
    return CustomPermission



class HasPropertyPermission(BasePermission):

    def __init__(self, perm_code):
        self.perm_code = perm_code

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        # Admin bypass
        if request.user.is_superuser or request.user.is_admin:
            return True

        profile = getattr(request.user, "profile", None)
        if not profile:
            return False

        # 🔥 Extract property_id
        property_id = (
            request.data.get("property_id") or
            request.query_params.get("property_id") or
            view.kwargs.get("property_id")
        )

        if not property_id:
            return False

        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return False

        # Check if user has access to this property
        if not profile.properties.filter(id=property_id).exists():
            return False

        return profile.has_permission(self.perm_code, property=property_obj)
    

def property_permission_required(code):
    class CustomPermission(HasPropertyPermission):
        def __init__(self):
            super().__init__(code)
    return CustomPermission