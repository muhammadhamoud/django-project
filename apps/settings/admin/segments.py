from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from settings.models.segments import SegmentGroup, SegmentCategory, Segment, SegmentDetail


class SegmentCategoryInline(admin.TabularInline):
    model = SegmentCategory
    extra = 0
    fields = ("code", "name", "sort_order")
    ordering = ("sort_order", "name")
    show_change_link = True


class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 0
    fields = ("code", "name", "sort_order")
    ordering = ("sort_order", "name")
    show_change_link = True


@admin.register(SegmentGroup)
class SegmentGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "property", "sort_order")
    list_filter = ("property",)
    search_fields = ("name", "code", "property__name", "property__resort_code")
    ordering = ("property__resort_code", "sort_order", "name")


@admin.register(SegmentCategory)
class SegmentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "group", "property", "sort_order")
    list_filter = ("group__property", "group")
    search_fields = (
        "name",
        "code",
        "group__name",
        "group__code",
        "group__property__name",
        "group__property__resort_code",
    )
    ordering = ("group__property__resort_code", "group__sort_order", "sort_order", "name")
    inlines = [SegmentInline]

    @admin.display(ordering="group__property__resort_code", description="Property")
    def property(self, obj):
        return obj.property


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category", "group", "property", "sort_order")
    list_filter = (
        "category__group__property",
        "category__group",
        "category",
    )
    search_fields = (
        "name",
        "code",
        "category__name",
        "category__code",
        "category__group__name",
        "category__group__code",
        "category__group__property__name",
        "category__group__property__resort_code",
    )
    ordering = (
        "category__group__property__resort_code",
        "category__group__sort_order",
        "category__sort_order",
        "sort_order",
        "name",
    )

    @admin.display(ordering="category__group__name", description="Group")
    def group(self, obj):
        return obj.group

    @admin.display(ordering="category__group__property__resort_code", description="Property")
    def property(self, obj):
        return obj.property


class SegmentDetailAdminForm(forms.ModelForm):
    class Meta:
        model = SegmentDetail
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["segment"].queryset = Segment.objects.none()

        property_obj = None

        # edit existing object
        if self.instance and self.instance.pk and self.instance.property_id:
            property_obj = self.instance.property

        # submitted form data
        elif "property" in self.data:
            try:
                property_id = int(self.data.get("property"))
                property_obj = property_id
            except (TypeError, ValueError):
                property_obj = None

        if property_obj:
            self.fields["segment"].queryset = Segment.objects.filter(
                category__group__property=property_obj
            ).select_related("category", "category__group")

    def clean(self):
        cleaned_data = super().clean()
        property_obj = cleaned_data.get("property")
        segment = cleaned_data.get("segment")

        if property_obj and segment and segment.property != property_obj:
            raise ValidationError({
                "segment": "Selected segment must belong to the selected property."
            })

        return cleaned_data


@admin.register(SegmentDetail)
class SegmentDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "property", "segment", "category", "group", "sort_order")
    list_filter = ("property", "segment__category__group", "segment__category", "segment")
    search_fields = (
        "name",
        "code",
        "property__name",
        "property__resort_code",
        "segment__name",
        "segment__code",
        "segment__category__name",
        "segment__category__code",
        "segment__category__group__name",
        "segment__category__group__code",
    )
    ordering = ("property__resort_code", "sort_order", "name")
    autocomplete_fields = ("property", "segment")

    @admin.display(ordering="segment__category__name", description="Category")
    def category(self, obj):
        return obj.category

    @admin.display(ordering="segment__category__group__name", description="Group")
    def group(self, obj):
        return obj.group