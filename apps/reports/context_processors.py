from .models import ReportGroup, Report
from .views import get_allowed_properties_for_user, get_selected_property_for_user


def get_report_menu_for_user(request):
    user = request.user
    allowed_properties = get_allowed_properties_for_user(user)
    selected_property = get_selected_property_for_user(request, user, allowed_properties)

    if not selected_property:
        return {
            "report_menu": [],
            "allowed_properties": allowed_properties,
            "selected_property": None,
        }

    groups = (
        ReportGroup.objects.filter(
            is_active=True,
            allowed_properties=selected_property,
        )
        .prefetch_related("reports")
        .distinct()
        .order_by("sort_order", "title")
    )

    report_menu = []

    for group in groups:
        reports = (
            group.reports.filter(
                is_active=True,
                allowed_properties=selected_property,
            )
            .distinct()
            .order_by("sort_order", "title")
        )

        if reports.exists():
            report_menu.append({
                "title": group.title,
                "slug": group.slug,
                "description": group.description,
                "icon": group.icon or "fas fa-folder",
                "color": group.color or "brand",
                "url": group.get_absolute_url() if hasattr(group, "get_absolute_url") else None,
                "items": [
                    {
                        "title": report.title,
                        "slug": report.slug,
                        "description": report.description,
                        "icon": report.icon or "fas fa-file-lines",
                        "color": report.color or "slate",
                        "url": report.get_absolute_url() if hasattr(report, "get_absolute_url") else None,
                        "group_slug": group.slug,
                    }
                    for report in reports
                ]
            })

    return {
        "report_menu": report_menu,
        "allowed_properties": allowed_properties,
        "selected_property": selected_property,
    }

def report_menu_context(request):
    if not request.user.is_authenticated:
        return {
            "report_menu": [],
            "allowed_properties": [],
            "selected_property": None,
        }

    return get_report_menu_for_user(request)