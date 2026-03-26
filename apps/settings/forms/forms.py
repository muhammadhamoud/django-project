from django import forms
from django.forms import BaseModelFormSet, modelformset_factory
from django.core.exceptions import ValidationError
from django.utils.text import capfirst


INPUT_CLASSES = (
    "block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 "
    "shadow-sm outline-none transition placeholder:text-slate-400 "
    "focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 "
    "dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:placeholder:text-slate-500 "
    "dark:focus:border-indigo-400 dark:focus:ring-indigo-400/20"
)

CHECKBOX_CLASSES = (
    "h-4 w-4 rounded border-slate-300 text-red-600 focus:ring-red-500/20 "
    "dark:border-slate-600 dark:bg-slate-900 dark:text-red-500"
)

DEFAULT_PLACEHOLDERS = {
    "code": "Enter code",
    "name": "Enter name",
    "sort_order": "0",
    "description": "Enter description",
}


class GenericBaseModelFormSet(BaseModelFormSet):
    required_new_row_fields = ["code", "name"]
    unique_together_check = ("property", "code")
    unique_together_message = "Duplicate codes are not allowed for the same property."
    reject_empty_new_rows = True

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        seen_values = set()
        has_empty_new_row = False

        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            instance_pk = form.cleaned_data.get("id")
            is_new_row = not instance_pk

            if is_new_row:
                has_any_user_value = False

                for field_name in self.required_new_row_fields:
                    value = form.cleaned_data.get(field_name)
                    if isinstance(value, str):
                        value = value.strip()
                    if value not in (None, "", []):
                        has_any_user_value = True
                        break

                if not has_any_user_value:
                    for field_name, value in form.cleaned_data.items():
                        if field_name in ("id", "DELETE"):
                            continue
                        if isinstance(value, str):
                            value = value.strip()
                        if value not in (None, "", []):
                            has_any_user_value = True
                            break

                if not has_any_user_value:
                    has_empty_new_row = True
                    continue

                missing_required = []
                for field_name in self.required_new_row_fields:
                    value = form.cleaned_data.get(field_name)
                    if isinstance(value, str):
                        value = value.strip()
                    if value in (None, "", []):
                        missing_required.append(field_name)

                if missing_required:
                    readable = ", ".join(missing_required)
                    raise ValidationError(f"New rows must include: {readable}.")

            if self.unique_together_check:
                unique_values = []
                can_check_unique = True

                for field_name in self.unique_together_check:
                    value = form.cleaned_data.get(field_name)
                    if isinstance(value, str):
                        value = value.strip().lower()

                    if value in (None, "", []):
                        can_check_unique = False
                        break

                    if hasattr(value, "pk"):
                        value = value.pk

                    unique_values.append(value)

                if can_check_unique:
                    key = tuple(unique_values)
                    if key in seen_values:
                        raise ValidationError(self.unique_together_message)
                    seen_values.add(key)

        if self.reject_empty_new_rows and has_empty_new_row:
            raise ValidationError(
                "Empty rows are not allowed. Please fill the new row or remove it before saving."
            )


def create_model_form(
    model_,
    fields_,
    hidden_fields=None,
    placeholders=None,
    form_name=None,
    scoped_foreign_keys=None,
):
    hidden_fields = hidden_fields or []
    placeholders = placeholders or {}
    scoped_foreign_keys = scoped_foreign_keys or {}

    class DynamicModelForm(forms.ModelForm):
        class Meta:
            model = model_
            fields = fields_

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name, bound_field in self.fields.items():
                if field_name in hidden_fields:
                    bound_field.widget = forms.HiddenInput()
                    continue

                if field_name in placeholders:
                    bound_field.widget.attrs["placeholder"] = placeholders[field_name]

                css_class = bound_field.widget.attrs.get("class", "")
                if isinstance(bound_field.widget, forms.CheckboxInput):
                    bound_field.widget.attrs["class"] = CHECKBOX_CLASSES
                else:
                    merged = f"{css_class} {INPUT_CLASSES}".strip()
                    bound_field.widget.attrs["class"] = merged

                    if "placeholder" not in bound_field.widget.attrs:
                        bound_field.widget.attrs["placeholder"] = placeholders.get(
                            field_name,
                            DEFAULT_PLACEHOLDERS.get(
                                field_name,
                                f"Enter {capfirst(field_name.replace('_', ' '))}"
                            )
                        )

                    if isinstance(bound_field.widget, forms.NumberInput):
                        bound_field.widget.attrs.setdefault("min", "0")

                    if not isinstance(
                        bound_field.widget,
                        (forms.Select, forms.CheckboxInput, forms.HiddenInput)
                    ):
                        bound_field.widget.attrs.setdefault("autocomplete", "off")

            for field_name, config in scoped_foreign_keys.items():
                if field_name not in self.fields:
                    continue

                related_model = config["model"]
                property_field = config.get("property_field", "property")
                related_property_field = config.get("related_property_field", "property")
                order_by = config.get("order_by", ("name",))

                self.fields[field_name].queryset = related_model.objects.none()

                property_id = None

                if self.is_bound:
                    property_id = self.data.get(property_field) or self.data.get(f"{property_field}_id")

                if not property_id:
                    property_id = self.initial.get(property_field) or self.initial.get(f"{property_field}_id")

                if not property_id and self.instance and self.instance.pk:
                    property_id = getattr(self.instance, f"{property_field}_id", None)

                if property_id:
                    self.fields[field_name].queryset = related_model.objects.filter(
                        **{f"{related_property_field}_id": property_id}
                    ).order_by(*order_by)

            # for field_name, config in scoped_foreign_keys.items():
            #     if field_name not in self.fields:
            #         continue

            #     related_model = config["model"]
            #     property_field = config.get("property_field", "property")
            #     related_property_field = config.get("related_property_field", "property")
            #     order_by = config.get("order_by", ("name",))

            #     self.fields[field_name].queryset = related_model.objects.none()

            #     property_id = None

            #     if self.is_bound:
            #         property_id = self.data.get(property_field) or self.data.get(f"{property_field}_id")

            #     if not property_id and self.instance and self.instance.pk:
            #         property_id = getattr(self.instance, f"{property_field}_id", None)

            #     if property_id:
            #         self.fields[field_name].queryset = related_model.objects.filter(
            #             **{f"{related_property_field}_id": property_id}
            #         ).order_by(*order_by)

    if form_name:
        DynamicModelForm.__name__ = form_name

    return DynamicModelForm


def create_formset_class(
    model,
    form_class,
    *,
    formset_name=None,
    required_new_row_fields=None,
    unique_together_check=("property", "code"),
    unique_together_message="Duplicate codes are not allowed for the same property.",
    reject_empty_new_rows=True,
    extra=0,
    can_delete=True,
):
    attrs = {
        "required_new_row_fields": required_new_row_fields or ["code", "name"],
        "unique_together_check": unique_together_check,
        "unique_together_message": unique_together_message,
        "reject_empty_new_rows": reject_empty_new_rows,
    }

    dynamic_formset_base = type(
        formset_name or f"{model.__name__}BaseFormSet",
        (GenericBaseModelFormSet,),
        attrs,
    )

    return modelformset_factory(
        model,
        form=form_class,
        formset=dynamic_formset_base,
        extra=extra,
        can_delete=can_delete,
    )



# from django import forms
# from django.forms import BaseModelFormSet, modelformset_factory
# from django.core.exceptions import ValidationError
# from django.utils.text import capfirst


# INPUT_CLASSES = (
#     "block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 "
#     "shadow-sm outline-none transition placeholder:text-slate-400 "
#     "focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 "
#     "dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:placeholder:text-slate-500 "
#     "dark:focus:border-indigo-400 dark:focus:ring-indigo-400/20"
# )

# CHECKBOX_CLASSES = (
#     "h-4 w-4 rounded border-slate-300 text-red-600 focus:ring-red-500/20 "
#     "dark:border-slate-600 dark:bg-slate-900 dark:text-red-500"
# )

# DEFAULT_PLACEHOLDERS = {
#     "code": "Enter code",
#     "name": "Enter name",
#     "sort_order": "0",
# }


# class GenericBaseModelFormSet(BaseModelFormSet):
#     required_new_row_fields = ["code", "name"]
#     unique_together_check = ("property", "code")
#     unique_together_message = "Duplicate codes are not allowed for the same property."
#     reject_empty_new_rows = True

#     def clean(self):
#         super().clean()

#         if any(self.errors):
#             return

#         seen_values = set()
#         has_empty_new_row = False

#         for form in self.forms:
#             if not hasattr(form, "cleaned_data") or not form.cleaned_data:
#                 continue

#             if form.cleaned_data.get("DELETE"):
#                 continue

#             instance_pk = form.cleaned_data.get("id")
#             is_new_row = not instance_pk

#             if is_new_row:
#                 has_any_user_value = False

#                 for field_name in self.required_new_row_fields:
#                     value = form.cleaned_data.get(field_name)
#                     if isinstance(value, str):
#                         value = value.strip()
#                     if value not in (None, "", []):
#                         has_any_user_value = True
#                         break

#                 # also inspect any other editable fields on the form
#                 if not has_any_user_value:
#                     for field_name, value in form.cleaned_data.items():
#                         if field_name in ("id", "DELETE"):
#                             continue
#                         if isinstance(value, str):
#                             value = value.strip()
#                         if value not in (None, "", []):
#                             has_any_user_value = True
#                             break

#                 if not has_any_user_value:
#                     has_empty_new_row = True
#                     continue

#                 missing_required = []
#                 for field_name in self.required_new_row_fields:
#                     value = form.cleaned_data.get(field_name)
#                     if isinstance(value, str):
#                         value = value.strip()
#                     if value in (None, "", []):
#                         missing_required.append(field_name)

#                 if missing_required:
#                     readable = ", ".join(missing_required)
#                     raise ValidationError(f"New rows must include: {readable}.")

#             if self.unique_together_check:
#                 unique_values = []
#                 can_check_unique = True

#                 for field_name in self.unique_together_check:
#                     value = form.cleaned_data.get(field_name)
#                     if isinstance(value, str):
#                         value = value.strip().lower()

#                     if value in (None, "", []):
#                         can_check_unique = False
#                         break

#                     if hasattr(value, "pk"):
#                         value = value.pk

#                     unique_values.append(value)

#                 if can_check_unique:
#                     key = tuple(unique_values)
#                     if key in seen_values:
#                         raise ValidationError(self.unique_together_message)
#                     seen_values.add(key)

#         if self.reject_empty_new_rows and has_empty_new_row:
#             raise ValidationError(
#                 "Empty rows are not allowed. Please fill the new row or remove it before saving."
#             )


# def build_widget_for_field(field_name, model_field):
#     if field_name == "property":
#         return forms.HiddenInput()

#     if isinstance(model_field, (forms.BooleanField,)):
#         return forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES})

#     if hasattr(model_field, "choices") and model_field.choices:
#         return forms.Select(attrs={"class": INPUT_CLASSES})

#     if isinstance(model_field, forms.IntegerField):
#         return forms.NumberInput(
#             attrs={
#                 "class": INPUT_CLASSES,
#                 "placeholder": DEFAULT_PLACEHOLDERS.get(field_name, f"Enter {field_name.replace('_', ' ')}"),
#                 "min": "0",
#             }
#         )

#     if isinstance(model_field.widget, forms.Textarea):
#         return forms.Textarea(
#             attrs={
#                 "class": INPUT_CLASSES,
#                 "placeholder": DEFAULT_PLACEHOLDERS.get(field_name, f"Enter {field_name.replace('_', ' ')}"),
#                 "rows": 3,
#             }
#         )

#     return forms.TextInput(
#         attrs={
#             "class": INPUT_CLASSES,
#             "placeholder": DEFAULT_PLACEHOLDERS.get(field_name, f"Enter {field_name.replace('_', ' ')}"),
#             "autocomplete": "off",
#         }
#     )


# def create_model_form(
#     model_,
#     fields_,
#     hidden_fields=None,
#     placeholders=None,
#     form_name=None,
# ):
#     hidden_fields = hidden_fields or []
#     placeholders = placeholders or {}

#     class DynamicModelForm(forms.ModelForm):
#         class Meta:
#             model = model_
#             fields = fields_

#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)

#             for field_name, bound_field in self.fields.items():
#                 if field_name in hidden_fields:
#                     bound_field.widget = forms.HiddenInput()
#                     continue

#                 if field_name in placeholders:
#                     bound_field.widget.attrs["placeholder"] = placeholders[field_name]

#                 css_class = bound_field.widget.attrs.get("class", "")
#                 if isinstance(bound_field.widget, forms.CheckboxInput):
#                     bound_field.widget.attrs["class"] = CHECKBOX_CLASSES
#                 else:
#                     merged = f"{css_class} {INPUT_CLASSES}".strip()
#                     bound_field.widget.attrs["class"] = merged

#                     if "placeholder" not in bound_field.widget.attrs:
#                         bound_field.widget.attrs["placeholder"] = placeholders.get(
#                             field_name,
#                             DEFAULT_PLACEHOLDERS.get(
#                                 field_name,
#                                 f"Enter {capfirst(field_name.replace('_', ' '))}"
#                             )
#                         )

#                     if isinstance(bound_field.widget, forms.NumberInput):
#                         bound_field.widget.attrs.setdefault("min", "0")

#                     if not isinstance(bound_field.widget, (forms.Select, forms.CheckboxInput, forms.HiddenInput)):
#                         bound_field.widget.attrs.setdefault("autocomplete", "off")

#     if form_name:
#         DynamicModelForm.__name__ = form_name

#     return DynamicModelForm


# def create_model_form_from_model_fields(
#     model,
#     fields,
#     hidden_fields=None,
#     placeholders=None,
#     form_name=None,
# ):
#     hidden_fields = hidden_fields or []
#     placeholders = placeholders or {}

#     meta_widgets = {}

#     temp_form = forms.modelform_factory(model, fields=fields)()
#     for field_name in fields:
#         bound_field = temp_form.fields[field_name]

#         if field_name in hidden_fields:
#             meta_widgets[field_name] = forms.HiddenInput()
#             continue

#         if isinstance(bound_field, forms.BooleanField):
#             meta_widgets[field_name] = forms.CheckboxInput(attrs={"class": CHECKBOX_CLASSES})
#         elif hasattr(bound_field, "choices") and bound_field.choices:
#             meta_widgets[field_name] = forms.Select(attrs={"class": INPUT_CLASSES})
#         elif isinstance(bound_field, forms.IntegerField):
#             meta_widgets[field_name] = forms.NumberInput(
#                 attrs={
#                     "class": INPUT_CLASSES,
#                     "placeholder": placeholders.get(field_name, DEFAULT_PLACEHOLDERS.get(field_name, f"Enter {field_name}")),
#                     "min": "0",
#                 }
#             )
#         else:
#             meta_widgets[field_name] = forms.TextInput(
#                 attrs={
#                     "class": INPUT_CLASSES,
#                     "placeholder": placeholders.get(field_name, DEFAULT_PLACEHOLDERS.get(field_name, f"Enter {field_name}")),
#                     "autocomplete": "off",
#                 }
#             )

#     class DynamicModelForm(forms.ModelForm):
#         class Meta:
#             model = model
#             fields = fields
#             widgets = meta_widgets

#     if form_name:
#         DynamicModelForm.__name__ = form_name

#     return DynamicModelForm


# def create_formset_class(
#     model,
#     form_class,
#     *,
#     formset_name=None,
#     required_new_row_fields=None,
#     unique_together_check=("property", "code"),
#     unique_together_message="Duplicate codes are not allowed for the same property.",
#     reject_empty_new_rows=True,
#     extra=0,
#     can_delete=True,
# ):
#     attrs = {
#         "required_new_row_fields": required_new_row_fields or ["code", "name"],
#         "unique_together_check": unique_together_check,
#         "unique_together_message": unique_together_message,
#         "reject_empty_new_rows": reject_empty_new_rows,
#     }

#     dynamic_formset_base = type(
#         formset_name or f"{model.__name__}BaseFormSet",
#         (GenericBaseModelFormSet,),
#         attrs,
#     )

#     return modelformset_factory(
#         model,
#         form=form_class,
#         formset=dynamic_formset_base,
#         extra=extra,
#         can_delete=can_delete,
#     )