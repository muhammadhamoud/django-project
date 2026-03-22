from django import forms
from django.forms import modelformset_factory

from .models import SegmentGroup, Segment, SubSegment, DetailSegment


class TailwindMixin:
    def apply_tailwind_classes(self):
        base = (
            "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 "
            "text-sm text-slate-900 shadow-sm focus:border-blue-500 "
            "focus:outline-none focus:ring-2 focus:ring-blue-200"
        )
        checkbox = "h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = checkbox
            else:
                current = widget.attrs.get("class", "")
                widget.attrs["class"] = f"{current} {base}".strip()


class SegmentGroupTableForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = SegmentGroup
        fields = ["name", "code", "description", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes()


class SegmentTableForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Segment
        fields = ["group", "name", "code", "description", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        property_obj = kwargs.pop("property_obj", None)
        super().__init__(*args, **kwargs)
        if property_obj:
            self.fields["group"].queryset = SegmentGroup.objects.filter(
                property=property_obj,
                is_active=True,
            ).order_by("sort_order", "name")
        self.apply_tailwind_classes()


class SubSegmentTableForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = SubSegment
        fields = ["segment", "name", "code", "description", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        property_obj = kwargs.pop("property_obj", None)
        super().__init__(*args, **kwargs)
        if property_obj:
            self.fields["segment"].queryset = Segment.objects.filter(
                group__property=property_obj,
                is_active=True,
            ).select_related("group").order_by("group__sort_order", "sort_order", "name")
        self.apply_tailwind_classes()


class DetailSegmentTableForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = DetailSegment
        fields = ["sub_segment", "name", "code", "description", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        property_obj = kwargs.pop("property_obj", None)
        super().__init__(*args, **kwargs)
        if property_obj:
            self.fields["sub_segment"].queryset = SubSegment.objects.filter(
                segment__group__property=property_obj,
                is_active=True,
            ).select_related("segment", "segment__group").order_by(
                "segment__group__sort_order", "segment__sort_order", "sort_order", "name"
            )
        self.apply_tailwind_classes()


SegmentFormSet = modelformset_factory(
    Segment,
    form=SegmentTableForm,
    extra=1,
    can_delete=True,
)

SubSegmentFormSet = modelformset_factory(
    SubSegment,
    form=SubSegmentTableForm,
    extra=1,
    can_delete=True,
)

DetailSegmentFormSet = modelformset_factory(
    DetailSegment,
    form=DetailSegmentTableForm,
    extra=1,
    can_delete=True,
)


from django import forms

from .models import SegmentGroup, Segment, SubSegment, DetailSegment
from properties.models import Property


class DetailSegmentAssignmentForm(forms.ModelForm):
    property = forms.ModelChoiceField(
        queryset=Property.objects.none(),
        required=True,
    )
    group = forms.ModelChoiceField(
        queryset=SegmentGroup.objects.none(),
        required=True,
    )
    segment = forms.ModelChoiceField(
        queryset=Segment.objects.none(),
        required=True,
    )
    sub_segment = forms.ModelChoiceField(
        queryset=SubSegment.objects.none(),
        required=True,
    )

    class Meta:
        model = DetailSegment
        fields = [
            "property",
            "group",
            "segment",
            "sub_segment",
            "name",
            "code",
            "description",
            "sort_order",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        allowed_properties = kwargs.pop("allowed_properties", Property.objects.none())
        super().__init__(*args, **kwargs)

        self.fields["property"].queryset = allowed_properties

        property_obj = None
        group_obj = None
        segment_obj = None

        if self.is_bound:
            property_id = self.data.get("property")
            group_id = self.data.get("group")
            segment_id = self.data.get("segment")

            if property_id:
                self.fields["group"].queryset = SegmentGroup.objects.filter(
                    property_id=property_id,
                    is_active=True,
                ).order_by("sort_order", "name")

            if group_id:
                self.fields["segment"].queryset = Segment.objects.filter(
                    group_id=group_id,
                    is_active=True,
                ).order_by("sort_order", "name")

            if segment_id:
                self.fields["sub_segment"].queryset = SubSegment.objects.filter(
                    segment_id=segment_id,
                    is_active=True,
                ).order_by("sort_order", "name")

        elif self.instance and self.instance.pk:
            sub_segment = self.instance.sub_segment
            segment = sub_segment.segment
            group = segment.group
            property_obj = group.property

            self.fields["property"].initial = property_obj
            self.fields["group"].queryset = SegmentGroup.objects.filter(
                property=property_obj,
                is_active=True,
            ).order_by("sort_order", "name")
            self.fields["group"].initial = group

            self.fields["segment"].queryset = Segment.objects.filter(
                group=group,
                is_active=True,
            ).order_by("sort_order", "name")
            self.fields["segment"].initial = segment

            self.fields["sub_segment"].queryset = SubSegment.objects.filter(
                segment=segment,
                is_active=True,
            ).order_by("sort_order", "name")
            self.fields["sub_segment"].initial = sub_segment

    def clean(self):
        cleaned_data = super().clean()
        property_obj = cleaned_data.get("property")
        group = cleaned_data.get("group")
        segment = cleaned_data.get("segment")
        sub_segment = cleaned_data.get("sub_segment")

        if group and property_obj and group.property_id != property_obj.id:
            self.add_error("group", "Selected group does not belong to the selected property.")

        if segment and group and segment.group_id != group.id:
            self.add_error("segment", "Selected segment does not belong to the selected group.")

        if sub_segment and segment and sub_segment.segment_id != segment.id:
            self.add_error("sub_segment", "Selected subsegment does not belong to the selected segment.")

        return cleaned_data