# reports/services/report_filters.py

from django.db.models import Q
from properties.models import Property
from django.core.exceptions import PermissionDenied
from reports.models import Report



def get_allowed_properties_for_user(user):
    if user.is_superuser or getattr(user, "is_admin", False):
        return Property.objects.all()

    if not hasattr(user, "profile"):
        return Property.objects.none()

    return user.profile.properties.filter(is_active=True).distinct()


def get_selected_property_for_user(request, user, allowed_properties):
    property_id = request.GET.get("property")

    if not allowed_properties.exists():
        return None

    if not property_id:
        return allowed_properties.first()

    selected_property = allowed_properties.filter(id=property_id).first()
    if not selected_property:
        raise PermissionDenied("You do not have access to this property.")
    return selected_property


def get_report_queryset_for_user(request, user):
    allowed_properties = get_allowed_properties_for_user(user)
    selected_property = get_selected_property_for_user(
        request,
        user,
        allowed_properties,
    )

    if not selected_property:
        return Report.objects.none(), allowed_properties, None

    queryset = (
        Report.objects.select_related("group")
        .prefetch_related(
            "allowed_properties",
            "group__allowed_properties",
        )
        .filter(
            is_active=True,
            group__is_active=True,
            group__allowed_properties=selected_property,
            allowed_properties=selected_property,
        )
        .distinct()
    )

    return queryset, allowed_properties, selected_property