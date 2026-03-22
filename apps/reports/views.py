from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import ReportGroup, Report
from properties.models import Property
from django.core.exceptions import PermissionDenied
from django.db import models


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



@login_required
def report_group_list_view(request):
    allowed_properties = get_allowed_properties_for_user(request.user)
    selected_property = get_selected_property_for_user(
        request,
        request.user,
        allowed_properties,
    )

    groups = ReportGroup.objects.filter(is_active=True).prefetch_related("allowed_properties")

    if selected_property:
        groups = groups.filter(allowed_properties=selected_property).distinct()
    else:
        groups = ReportGroup.objects.none()

    # for group in groups:
    #     print(list(group.allowed_properties.all()))

    return render(
        request,
        "reports/group_list.html",
        {
            "groups": groups,
            "allowed_properties": allowed_properties,
            "selected_property": selected_property,
        },
    )


# @login_required
# def report_group_list_view(request):
#     user_properties = request.user.profile.properties.all()

#     groups = ReportGroup.objects.filter(is_active=True).prefetch_related(
#         "allowed_properties"
#     )

#     visible_groups = []
#     for group in groups:
#         if not group.allowed_properties.exists():
#             visible_groups.append(group)
#         elif group.allowed_properties.filter(id__in=user_properties.values_list("id", flat=True)).exists():
#             visible_groups.append(group)

#     return render(request, "reports/group_list.html", {
#         "groups": visible_groups,
#     })


@login_required
def report_list_by_group_view(request, slug):
    allowed_properties = get_allowed_properties_for_user(request.user)
    selected_property = get_selected_property_for_user(
        request,
        request.user,
        allowed_properties,
    )

    if not selected_property:
        messages.error(request, "No property assigned.")
        return redirect("reports:group_list")

    group = get_object_or_404(
        ReportGroup.objects.prefetch_related(
            "allowed_properties",
            "reports__allowed_properties",
        ),
        slug=slug,
        is_active=True,
        allowed_properties=selected_property,
    )

    reports = group.reports.filter(
        is_active=True,
        allowed_properties=selected_property,
    ).distinct()

    return render(
        request,
        "reports/report_list.html",
        {
            "group": group,
            "reports": reports,
            "page_title": group.title,
            "page_subtitle": group.description or "Browse available reports in this group.",
            "allowed_properties": allowed_properties,
            "selected_property": selected_property,
        },
    )

# @login_required
# def report_list_by_group_view(request, slug):
#     user_properties = request.user.profile.properties.all()
#     user_property_ids = user_properties.values_list("id", flat=True)

#     group = get_object_or_404(
#         ReportGroup.objects.prefetch_related("allowed_properties", "reports__allowed_properties"),
#         slug=slug,
#         is_active=True
#     )

#     if group.allowed_properties.exists() and not group.allowed_properties.filter(id__in=user_property_ids).exists():
#         messages.error(request, "Permission denied")
#         return redirect("reports:group_list")

#     reports = group.reports.filter(is_active=True)
#     visible_reports = []

#     for report in reports:
#         if not report.allowed_properties.exists():
#             visible_reports.append(report)
#         elif report.allowed_properties.filter(id__in=user_property_ids).exists():
#             visible_reports.append(report)

#     return render(request, "reports/report_list.html", {
#         "group": group,
#         "reports": visible_reports,
#         "page_title": group.title,
#         "page_subtitle": group.description or "Browse available reports in this group.",
        
#     })

@login_required
def report_detail_view(request, group_slug, report_slug):
    allowed_properties = get_allowed_properties_for_user(request.user)
    selected_property = get_selected_property_for_user(
        request,
        request.user,
        allowed_properties,
    )

    if not selected_property:
        messages.error(request, "No property assigned.")
        return redirect("reports:group_list")

    report = get_object_or_404(
        Report.objects.select_related("group").prefetch_related(
            "allowed_properties",
            "group__allowed_properties",
        ),
        group__slug=group_slug,
        slug=report_slug,
        is_active=True,
        group__is_active=True,
        group__allowed_properties=selected_property,
        allowed_properties=selected_property,
    )

    embed_token = ""

    return render(
        request,
        "reports/report_detail.html",
        {
            "report": report,
            "page_title": report.title,
            "page_subtitle": report.description or "Power BI report details.",
            "allowed_properties": allowed_properties,
            "selected_property": selected_property,
            "powerbi_config": {
                "report_id": report.powerbi_report_id,
                "embed_url": report.powerbi_embed_url,
                "embed_token": embed_token,
            },
        },
    )


# @login_required
# def report_detail_view(request, group_slug, report_slug):
#     user_properties = request.user.profile.properties.all()
#     user_property_ids = user_properties.values_list("id", flat=True)

#     report = get_object_or_404(
#         Report.objects.select_related("group").prefetch_related(
#             "allowed_properties",
#             "group__allowed_properties",
#         ),
#         group__slug=group_slug,
#         slug=report_slug,
#         is_active=True,
#         group__is_active=True,
#     )

#     if report.group.allowed_properties.exists():
#         if not report.group.allowed_properties.filter(id__in=user_property_ids).exists():
#             messages.error(request, "Permission denied")
#             return redirect("reports:group_list")

#     if report.allowed_properties.exists():
#         if not report.allowed_properties.filter(id__in=user_property_ids).exists():
#             messages.error(request, "Permission denied")
#             return redirect("reports:group_list")

#     # This should come from your Power BI token service
#     embed_token = ""

#     # Example:
#     # embed_token = generate_powerbi_embed_token(
#     #     report_id=report.powerbi_report_id,
#     #     workspace_id=report.powerbi_workspace_id,
#     # )

#     return render(request, "reports/report_detail.html", {
#         "report": report,
#         "page_title": report.title,
#         "page_subtitle": report.description or "Power BI report details.",
#             "powerbi_config": {
#             "report_id": report.powerbi_report_id,
#             "embed_url": report.powerbi_embed_url,
#             "embed_token": embed_token,
#         }
#     })

