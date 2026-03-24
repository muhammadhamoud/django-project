from django import forms
from django.forms import BaseModelFormSet, modelformset_factory
from django.core.exceptions import ValidationError

from settings.models.segments import SegmentGroup


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


class SegmentGroupForm(forms.ModelForm):
    class Meta:
        model = SegmentGroup
        fields = ["property", "code", "name", "sort_order"]
        widgets = {
            "property": forms.HiddenInput(),
            "code": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Enter code",
                    "autocomplete": "off",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Enter name",
                    "autocomplete": "off",
                }
            ),
            "sort_order": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "0",
                    "min": "0",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "DELETE" in self.fields:
            self.fields["DELETE"].widget.attrs.update({"class": CHECKBOX_CLASSES})


class BaseSegmentGroupFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        seen_codes = set()

        for form in self.forms:
            if not getattr(form, "cleaned_data", None):
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            property_obj = form.cleaned_data.get("property")
            code = (form.cleaned_data.get("code") or "").strip().lower()

            if not property_obj or not code:
                continue

            key = (property_obj.pk, code)
            if key in seen_codes:
                raise ValidationError(
                    "Duplicate segment group codes are not allowed for the same property."
                )
            seen_codes.add(key)


SegmentGroupFormSet = modelformset_factory(
    SegmentGroup,
    form=SegmentGroupForm,
    formset=BaseSegmentGroupFormSet,
    extra=0,
    can_delete=True,
)