from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import ReportGroup, Report
from .services.report_filters import get_allowed_properties_for_user, get_selected_property_for_user
from reports.services.report_filters import get_report_queryset_for_user


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



from django.http import JsonResponse
from django.db.models import Q
from reports.services.report_filters import get_report_queryset_for_user


@login_required
def report_autocomplete(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({"results": []})

    reports_qs, allowed_properties, selected_property = get_report_queryset_for_user(
        request,
        request.user,
    )

    if not selected_property:
        return JsonResponse({"results": []})

    reports = (
        reports_qs.filter(
            Q(title__icontains=query) |
            Q(slug__icontains=query) |
            Q(group__title__icontains=query) |
            Q(group__title__icontains=query) |
            Q(description__icontains=query)
        )
        .order_by("group__title", "title")[:10]
    )

    return JsonResponse({
        "results": [
            {
                "name": report.title,
                "url": report.get_absolute_url(),
                "group": getattr(report.group, "title", None) or getattr(report.group, "name", ""),
            }
            for report in reports
        ]
    })