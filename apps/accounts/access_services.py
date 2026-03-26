from django.core.exceptions import PermissionDenied
from properties.models import Property

FULL_ACCESS_ROLES = {"supervisor", "super_admin"}
EDIT_ACCESS_ROLES = {"property_admin", "supervisor", "super_admin"}


def get_user_role(user):
    if not user or not user.is_authenticated:
        return ""

    role = getattr(user, "role", None)
    if role is None and hasattr(user, "profile"):
        role = getattr(user.profile, "role", None)

    return (role or "").strip().lower()


def user_has_full_property_access(user):
    role = get_user_role(user)
    return (
        bool(user and user.is_authenticated)
        and (
            user.is_superuser
            or getattr(user, "is_admin", False)
            or role in FULL_ACCESS_ROLES
        )
    )


def user_can_edit_properties(user):
    role = get_user_role(user)
    return (
        bool(user and user.is_authenticated)
        and (
            user.is_superuser
            or getattr(user, "is_admin", False)
            or role in EDIT_ACCESS_ROLES
        )
    )


def get_allowed_properties_for_user(user):
    if not user or not user.is_authenticated:
        return Property.objects.none()

    if user_has_full_property_access(user):
        return Property.objects.filter(is_active=True).order_by("resort_code", "name")

    if not hasattr(user, "profile"):
        return Property.objects.none()

    return user.profile.properties.filter(is_active=True).distinct().order_by(
        "resort_code", "name"
    )


def user_can_view_property(user, property_obj):
    if not user or not user.is_authenticated or not property_obj:
        return False

    if user_has_full_property_access(user):
        return True

    if not hasattr(user, "profile"):
        return False

    return user.profile.properties.filter(pk=property_obj.pk, is_active=True).exists()


def user_can_edit_property(user, property_obj):
    if not user_can_view_property(user, property_obj):
        return False

    return user_can_edit_properties(user)


def get_selected_property_for_user(request, user, allowed_properties, field_name="property"):
    property_id = request.GET.get(field_name) or request.POST.get(field_name)

    if not allowed_properties.exists():
        return None

    if not property_id:
        return allowed_properties.first()

    selected_property = allowed_properties.filter(id=property_id).first()
    if not selected_property:
        raise PermissionDenied("You do not have access to this property.")

    return selected_property


def require_property_view_access(user, property_obj):
    if not user_can_view_property(user, property_obj):
        raise PermissionDenied("You do not have permission to view this property.")


def require_property_edit_access(user, property_obj):
    if not user_can_edit_property(user, property_obj):
        raise PermissionDenied("You do not have permission to edit this property.")