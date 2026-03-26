from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from settings.models import SettingsMenu
from reports.services.report_filters import (
    get_allowed_properties_for_user,
    get_selected_property_for_user,
)


@login_required
def settings_menu_list_view(request):
    allowed_properties = get_allowed_properties_for_user(request.user)
    selected_property = get_selected_property_for_user(
        request,
        request.user,
        allowed_properties,
    )

    groups = SettingsMenu.objects.filter(is_active=True).prefetch_related("allowed_properties")

    if selected_property:
        groups = groups.filter(
            models.Q(allowed_properties=selected_property) |
            models.Q(allowed_properties__isnull=True)
        ).distinct()
    else:
        groups = SettingsMenu.objects.none()

    return render(
        request,
        "settings/menu/menu_list.html",
        {
            "groups": groups,
            "allowed_properties": allowed_properties,
            "selected_property": selected_property,
        },
    )


@login_required
def settings_menu_items_view(request, slug):
    allowed_properties = get_allowed_properties_for_user(request.user)
    selected_property = get_selected_property_for_user(
        request,
        request.user,
        allowed_properties,
    )

    group = get_object_or_404(
        SettingsMenu.objects.filter(is_active=True).prefetch_related("allowed_properties"),
        slug=slug,
    )

    if not selected_property:
        raise Http404("No property selected.")

    if group.allowed_properties.exists() and not group.allowed_properties.filter(id=selected_property.id).exists():
        raise Http404("This settings menu is not available for the selected property.")

    return render(
        request,
        "settings/menu/menu_items.html",
        {
            "group": group,
            "allowed_properties": allowed_properties,
            "selected_property": selected_property,
        },
    )