from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from settings.models.segments import SegmentGroup
from settings.forms.segments import SegmentGroupFormSet
from accounts.access_services import (
    get_allowed_properties_for_user,
    get_selected_property_for_user,
)


@login_required
def segment_group_manage_view(request):
    allowed_properties = get_allowed_properties_for_user(request.user)
    selected_property = get_selected_property_for_user(
        request,
        request.user,
        allowed_properties,
    )

    if not selected_property:
        return render(
            request,
            "settings/segments/segment_group_manage.html",
            {
                "allowed_properties": allowed_properties,
                "selected_property": None,
                "formset": None,
                "page_obj": None,
                "paginator": None,
                "page_size": 30,
            },
        )

    page_size = request.GET.get("page_size") or request.POST.get("page_size") or 30
    page_number = request.GET.get("page") or request.POST.get("page") or 1

    try:
        page_size = int(page_size)
    except (TypeError, ValueError):
        page_size = 30

    if page_size not in [30, 50, 100]:
        page_size = 30

    base_queryset = SegmentGroup.objects.filter(
        property_id=selected_property.id
    ).order_by("sort_order", "name")

    paginator = Paginator(base_queryset, page_size)
    page_obj = paginator.get_page(page_number)

    page_queryset = page_obj.object_list

    if request.method == "POST":
        formset = SegmentGroupFormSet(request.POST, queryset=page_queryset)

        for form in formset.forms:
            form.fields["property"].initial = selected_property.pk
        formset.empty_form.fields["property"].initial = selected_property.pk

        if formset.is_valid():
            # Delete selected existing rows
            for form in formset.deleted_forms:
                instance = form.instance
                if instance.pk:
                    if instance.property_id != selected_property.id:
                        raise PermissionDenied("You do not have access to this property.")
                    instance.delete()

            # Save updated existing rows and new rows
            for form in formset.forms:
                if not getattr(form, "cleaned_data", None):
                    continue

                if form in formset.deleted_forms:
                    continue

                # Skip untouched blank extra rows
                if not form.has_changed() and not form.instance.pk:
                    continue

                code = (form.cleaned_data.get("code") or "").strip()
                name = (form.cleaned_data.get("name") or "").strip()
                property_obj = form.cleaned_data.get("property")

                # Skip new rows with no real data
                if not form.instance.pk and not any([code, name]):
                    continue

                if property_obj != selected_property:
                    raise PermissionDenied("Invalid property submitted.")

                instance = form.save(commit=False)
                instance.property = selected_property
                instance.save()

            messages.success(request, "Segment groups updated successfully.")
            return redirect(
                f"/segment-groups/manage/?property={selected_property.id}&page={page_obj.number}&page_size={page_size}"
            )
    else:
        formset = SegmentGroupFormSet(queryset=page_queryset)

        for form in formset.forms:
            form.fields["property"].initial = selected_property.pk
        formset.empty_form.fields["property"].initial = selected_property.pk

    return render(
        request,
        "settings/segments/segment_group_manage.html",
        {
            "allowed_properties": allowed_properties,
            "selected_property": selected_property,
            "formset": formset,
            "page_obj": page_obj,
            "paginator": paginator,
            "page_size": page_size,
        },
    )


