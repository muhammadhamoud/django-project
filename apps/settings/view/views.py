from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.utils.text import capfirst

from settings.models import SegmentGroup, Property
# from settings.forms import SegmentGroupForm, SegmentGroupFormSet
from settings.models import SegmentCategory, SegmentGroup
from settings.forms import create_model_form, create_formset_class

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from accounts.permissions import (
    get_allowed_properties_for_user,
    get_selected_property_for_user,
    require_property_view_access,
    require_property_edit_access,
)

page_size_options = [10, 20, 30, 40]

SegmentCategoryForm = create_model_form(
    model_=SegmentCategory,
    fields_=[
        "property",
        "group",
        "name",
        "code",
        "description",
        "is_active",
        "sort_order",
    ],
    placeholders={
        "name": "Enter name",
        "code": "Enter code",
        "description": "Enter description",
        "sort_order": "0",
    },
    form_name="SegmentCategoryForm",
    scoped_foreign_keys={
        "group": {
            "model": SegmentGroup,
            "property_field": "property",
            "related_property_field": "property",
            "order_by": ("sort_order", "name"),
        }
    },
)

SegmentCategoryFormSet = create_formset_class(
    model=SegmentCategory,
    form_class=SegmentCategoryForm,
    formset_name="BaseSegmentCategoryFormSet",
    required_new_row_fields=["code", "name"],
    unique_together_check=("property", "code"),
    unique_together_message="Duplicate segment category codes are not allowed for the same property.",
    extra=0,
    can_delete=True,
)

SegmentGroupForm = create_model_form(
    model_=SegmentGroup,
    fields_=[
        "property",
        "name",
        "code",
        "description",
        "is_active",
        "sort_order",
    ],
    placeholders={
        "name": "Enter name",
        "code": "Enter code",
        "description": "Enter description",
        "sort_order": "0",
    },
    form_name="SegmentGroupForm",
    scoped_foreign_keys={
        "group": {
            # "model": SegmentGroup,
            "property_field": "property",
            "related_property_field": "property",
            "order_by": ("sort_order", "name"),
        }
    },
)

SegmentGroupFormSet = create_formset_class(
    model=SegmentGroup,
    form_class=SegmentGroupForm,
    formset_name="BaseSegmentGroupFormSet",
    required_new_row_fields=["code", "name"],
    unique_together_check=("property", "code"),
    unique_together_message="Duplicate segment Group codes are not allowed for the same property.",
    extra=0,
    can_delete=True,
)


ENTITY_CONFIG = {
    "segmentcategory": {
        "model": SegmentCategory,
        "form": SegmentCategoryForm,
        "formset_class": SegmentCategoryFormSet,
        "title": "Segment Category",
        "filter_field": "property",
        "filter_label": "Property",
        "filter_queryset": lambda request: get_allowed_properties_for_user(request.user),
        "order_by": ["sort_order", "id"],
        "fields": ["code", "name", "description", "group", "is_active", "sort_order"],
        "bulk_fields": ["name", "group", "is_active"],
        "template": "settings/components/main_page.html",
        "page_size_options": page_size_options,
        "extra": 0,
        "can_delete": True,
    },
    "segmentgroup": {
        "model": SegmentGroup,
        "form": SegmentGroupForm,
        "formset_class": SegmentGroupFormSet,
        "title": "Segment Group",
        "filter_field": "property",
        "filter_label": "Property",
        "filter_queryset": lambda request: get_allowed_properties_for_user(request.user),
        "order_by": ["sort_order", "id"],
        "fields": ["code", "name", "description", "is_active", "sort_order"],
        "bulk_fields": ["name", "is_active"],
        "template": "settings/components/main_page.html",
        "page_size_options": page_size_options,
        "extra": 0,
        "can_delete": True,

    },
}

def get_entity_config(entity_key):
    config = ENTITY_CONFIG.get(entity_key)
    if not config:
        raise Http404("Invalid settings entity.")
    return config


def build_table_columns(form_class, field_names):
    form = form_class()
    columns = []

    for field_name in field_names:
        field = form.fields[field_name]
        widget = field.widget
        widget_class_name = widget.__class__.__name__
        input_type = getattr(widget, "input_type", "text")

        if field_name == "code":
            width = "w-20"
        elif field_name == "name":
            width = "w-[35%]"
        elif field_name in ("sort_order", "seq", "sequence"):
            width = "w-20"
        elif input_type == "checkbox":
            width = "w-24"
        elif widget_class_name == "Select":
            width = "w-32"
        else:
            width = "w-32"

        align = "text-center" if input_type == "checkbox" else "text-left"
        placeholder = "No" if input_type == "checkbox" else "—"

        columns.append({
            "name": field_name,
            "label": field.label or capfirst(field_name.replace("_", " ")),
            "width": width,
            "align": align,
            "placeholder": placeholder,
        })

    return columns



def build_bulk_fields(form_class, bulk_field_names, initial=None):
    form = form_class(initial=initial or {})
    bulk_fields = []

    for field_name in bulk_field_names:
        field = form.fields[field_name]
        widget = field.widget
        widget_class_name = widget.__class__.__name__
        input_type = getattr(widget, "input_type", "text")
        label = field.label or capfirst(field_name.replace("_", " "))

        if widget_class_name == "Select" or getattr(field, "choices", None):
            choices = []
            for value, choice_label in field.choices:
                if value in ("", None):
                    continue
                choices.append({
                    "value": value,
                    "label": str(choice_label),
                })

            bulk_fields.append({
                "name": field_name,
                "label": f"Bulk update {label}",
                "type": "select",
                "placeholder": f"Select {label}",
                "choices": choices,
            })

        elif input_type == "checkbox":
            bulk_fields.append({
                "name": field_name,
                "label": f"Bulk update {label}",
                "type": "checkbox",
                "checkbox_label": f"Set {label}",
            })

        elif widget_class_name == "Textarea":
            bulk_fields.append({
                "name": field_name,
                "label": f"Bulk update {label}",
                "type": "textarea",
                "placeholder": f"Enter {label}",
            })

        else:
            bulk_fields.append({
                "name": field_name,
                "label": f"Bulk update {label}",
                "type": "text",
                "placeholder": f"Enter {label}",
            })

    return bulk_fields


# def build_bulk_fields(form_class, bulk_field_names):
#     form = form_class()
    # bulk_fields = []

    # for field_name in bulk_field_names:
    #     field = form.fields[field_name]
    #     widget = field.widget
    #     widget_class_name = widget.__class__.__name__
    #     input_type = getattr(widget, "input_type", "text")
    #     label = field.label or capfirst(field_name.replace("_", " "))

    #     if widget_class_name == "Select" or getattr(field, "choices", None):
    #         choices = []
    #         for value, choice_label in field.choices:
    #             if value in ("", None):
    #                 continue
    #             choices.append({
    #                 "value": value,
    #                 "label": str(choice_label),
    #             })

    #         bulk_fields.append({
    #             "name": field_name,
    #             "label": f"Bulk update {label}",
    #             "type": "select",
    #             "placeholder": f"Select {label}",
    #             "choices": choices,
    #         })

    #     elif input_type == "checkbox":
    #         bulk_fields.append({
    #             "name": field_name,
    #             "label": f"Bulk update {label}",
    #             "type": "checkbox",
    #             "checkbox_label": f"Set {label}",
    #         })

    #     elif widget_class_name == "Textarea":
    #         bulk_fields.append({
    #             "name": field_name,
    #             "label": f"Bulk update {label}",
    #             "type": "textarea",
    #             "placeholder": f"Enter {label}",
    #         })

    #     else:
    #         bulk_fields.append({
    #             "name": field_name,
    #             "label": f"Bulk update {label}",
    #             "type": "text",
    #             "placeholder": f"Enter {label}",
    #         })

    # return bulk_fields


# def generic_settings_view(request, entity_key):
#     config = get_entity_config(entity_key)

#     model = config["model"]
#     form_class = config["form"]
#     formset_class = config.get("formset_class")
#     entity_title = config["title"]
#     filter_field = config["filter_field"]
#     filter_label = config.get("filter_label", capfirst(filter_field.replace("_", " ")))
#     filter_options = config["filter_queryset"](request)
#     order_by = config.get("order_by", ["id"])
#     table_field_names = config.get("fields") or list(form_class().fields.keys())
#     bulk_field_names = config.get("bulk_fields", [])
#     template_name = config.get("template", "settings/components/main_page.html")
#     page_size_options = config.get("page_size_options", [30, 50, 100])
#     extra = config.get("extra", 0)
#     can_delete = config.get("can_delete", True)

#     selected_filter_id = request.GET.get(filter_field) or request.POST.get(filter_field)
#     selected_filter = None

#     requested_page_size = request.GET.get("page_size") or request.POST.get("page_size") or page_size_options[0]
#     page_size = int(requested_page_size) if str(requested_page_size).isdigit() else page_size_options[0]
#     if page_size not in page_size_options:
#         page_size = page_size_options[0]

#     requested_page = request.GET.get("page") or request.POST.get("page") or 1
#     page_number = int(requested_page) if str(requested_page).isdigit() else 1

#     if formset_class is None:
#         FormSet = modelformset_factory(
#             model,
#             form=form_class,
#             extra=extra,
#             can_delete=can_delete,
#         )
#     else:
#         FormSet = formset_class

#     formset = None
#     page_obj = None
#     paginator = None

#     if selected_filter_id:
#         selected_filter = filter_options.filter(id=selected_filter_id).first()

#         if selected_filter:
#             queryset = model.objects.filter(**{filter_field: selected_filter}).order_by(*order_by)

#             paginator = Paginator(queryset, page_size)
#             page_obj = paginator.get_page(page_number)

#             if request.method == "POST":
#                 formset = FormSet(
#                     request.POST,
#                     queryset=page_obj.object_list,
#                     prefix="form",
#                 )

#                 if formset.is_valid():
#                     instances = formset.save(commit=False)

#                     if can_delete and hasattr(formset, "deleted_objects"):
#                         for obj in formset.deleted_objects:
#                             obj.delete()

#                     for instance in instances:
#                         relation_id_attr = f"{filter_field}_id"
#                         if hasattr(instance, relation_id_attr) and not getattr(instance, relation_id_attr):
#                             setattr(instance, filter_field, selected_filter)
#                         instance.save()

#                     if hasattr(formset, "save_m2m"):
#                         formset.save_m2m()

#                     messages.success(request, f"{entity_title} changes saved successfully.")
#                     return redirect(
#                         f"{request.path}?{filter_field}={selected_filter.id}&page={page_number}&page_size={page_size}"
#                     )
#                 else:
#                     messages.error(request, "Please correct the errors below.")
#             else:
#                 formset = FormSet(
#                     queryset=page_obj.object_list,
#                     prefix="form",
#                 )

#     table_columns = build_table_columns(form_class, table_field_names)
#     # bulk_fields = build_bulk_fields(form_class, bulk_field_names)
#     bulk_fields = build_bulk_fields(
#         form_class,
#         bulk_field_names,
#         initial={filter_field: selected_filter.id} if selected_filter else {},
#     )

#     context = {
#         "entity_key": entity_key,
#         "entity_title": entity_title,
#         "filter_field": filter_field,
#         "filter_label": filter_label,
#         "filter_options": filter_options,
#         "selected_filter": selected_filter,
#         "formset": formset,
#         "page_obj": page_obj,
#         "paginator": paginator,
#         "page_size": page_size,
#         "page_size_options": page_size_options,
#         "table_columns": table_columns,
#         "bulk_fields": bulk_fields,
#     }
#     return render(request, template_name, context)


@login_required
def generic_settings_view(request, entity_key):
    config = get_entity_config(entity_key)

    model = config["model"]
    form_class = config["form"]
    formset_class = config.get("formset_class")
    entity_title = config["title"]
    filter_field = config["filter_field"]
    filter_label = config.get("filter_label", capfirst(filter_field.replace("_", " ")))
    order_by = config.get("order_by", ["id"])
    table_field_names = config.get("fields") or list(form_class().fields.keys())
    bulk_field_names = config.get("bulk_fields", [])
    template_name = config.get("template", "settings/components/main_page.html")
    page_size_options = config.get("page_size_options", [30, 50, 100])
    extra = config.get("extra", 0)
    can_delete = config.get("can_delete", True)

    # Restrict property list by user
    filter_options = get_allowed_properties_for_user(request.user)

    # selected_filter = get_selected_property_for_user(
    #     request,
    #     request.user,
    #     filter_options,
    #     field_name=filter_field,
    # )

    # if selected_filter:
    #     require_property_view_access(request.user, selected_filter)

    selected_filter = get_selected_property_for_user(
        request,
        request.user,
        filter_options,
        field_name=filter_field,
    )

    if selected_filter and not require_property_view_access(request, request.user, selected_filter):
        selected_filter = None

    requested_page_size = request.GET.get("page_size") or request.POST.get("page_size") or page_size_options[0]
    page_size = int(requested_page_size) if str(requested_page_size).isdigit() else page_size_options[0]
    if page_size not in page_size_options:
        page_size = page_size_options[0]

    requested_page = request.GET.get("page") or request.POST.get("page") or 1
    page_number = int(requested_page) if str(requested_page).isdigit() else 1

    if formset_class is None:
        FormSet = modelformset_factory(
            model,
            form=form_class,
            extra=extra,
            can_delete=can_delete,
        )
    else:
        FormSet = formset_class

    formset = None
    page_obj = None
    paginator = None
    can_edit = False

    if selected_filter:
        queryset = model.objects.filter(**{filter_field: selected_filter}).order_by(*order_by)

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        can_edit = True
        try:
            if not require_property_edit_access(request, request.user, selected_filter):
                return redirect('dashboard:home')
        except PermissionDenied:
            can_edit = False

        if request.method == "POST":
            if not require_property_edit_access(request, request.user, selected_filter):
                return redirect('dashboard:home')

            formset = FormSet(
                request.POST,
                queryset=page_obj.object_list,
                prefix="form",
            )

            if formset.is_valid():
                instances = formset.save(commit=False)

                if can_delete and hasattr(formset, "deleted_objects"):
                    for obj in formset.deleted_objects:
                        obj.delete()

                for instance in instances:
                    relation_id_attr = f"{filter_field}_id"
                    if hasattr(instance, relation_id_attr) and not getattr(instance, relation_id_attr):
                        setattr(instance, filter_field, selected_filter)
                    instance.save()

                if hasattr(formset, "save_m2m"):
                    formset.save_m2m()

                messages.success(request, f"{entity_title} changes saved successfully.")
                return redirect(
                    f"{request.path}?{filter_field}={selected_filter.id}&page={page_number}&page_size={page_size}"
                )
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            formset = FormSet(
                queryset=page_obj.object_list,
                prefix="form",
            )

    table_columns = build_table_columns(form_class, table_field_names)
    bulk_fields = build_bulk_fields(
        form_class,
        bulk_field_names,
        initial={filter_field: selected_filter.id} if selected_filter else {},
    )

    context = {
        "entity_key": entity_key,
        "entity_title": entity_title,
        "filter_field": filter_field,
        "filter_label": filter_label,
        "filter_options": filter_options,
        "selected_filter": selected_filter,
        "formset": formset,
        "page_obj": page_obj,
        "paginator": paginator,
        "page_size": page_size,
        "page_size_options": page_size_options,
        "table_columns": table_columns,
        "bulk_fields": bulk_fields,
        "can_edit": can_edit,
    }
    return render(request, template_name, context)


def segment_group_view(request):
    return generic_settings_view(request, "segmentgroup")

def segment_category_view(request):
    return generic_settings_view(request, "segmentcategory")