from django.contrib import admin

from .models import SegmentGroup, Segment, SubSegment, DetailSegment


class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 0
    fields = ("name", "code", "description", "sort_order", "is_active")
    ordering = ("sort_order", "name")


@admin.register(SegmentGroup)
class SegmentGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "property",
        "code",
        "sort_order",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("property", "is_active")
    search_fields = (
        "name",
        "code",
        "description",
        "property__name",
        "property__hotel_code",
        "property__resort_code",
    )
    ordering = ("property__resort_code", "sort_order", "name")
    fields = ("property", "name", "code", "description", "sort_order", "is_active")
    inlines = [SegmentInline]


class SubSegmentInline(admin.TabularInline):
    model = SubSegment
    extra = 0
    fields = ("name", "code", "description", "sort_order", "is_active")
    ordering = ("sort_order", "name")


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
        "property_name",
        "code",
        "sort_order",
        "is_active",
    )
    list_filter = ("group__property", "is_active")
    search_fields = (
        "name",
        "code",
        "description",
        "group__name",
        "group__property__name",
        "group__property__hotel_code",
        "group__property__resort_code",
    )
    ordering = ("group__property__resort_code", "group__sort_order", "sort_order", "name")
    fields = ("group", "name", "code", "description", "sort_order", "is_active")
    inlines = [SubSegmentInline]

    @admin.display(description="Property")
    def property_name(self, obj):
        return obj.property


class DetailSegmentInline(admin.TabularInline):
    model = DetailSegment
    extra = 0
    fields = ("name", "code", "description", "sort_order", "is_active")
    ordering = ("sort_order", "name")


@admin.register(SubSegment)
class SubSegmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "segment",
        "property_name",
        "code",
        "sort_order",
        "is_active",
    )
    list_filter = ("segment__group__property", "is_active")
    search_fields = (
        "name",
        "code",
        "description",
        "segment__name",
        "segment__group__name",
        "segment__group__property__name",
        "segment__group__property__hotel_code",
        "segment__group__property__resort_code",
    )
    ordering = (
        "segment__group__property__resort_code",
        "segment__group__sort_order",
        "segment__sort_order",
        "sort_order",
        "name",
    )
    fields = ("segment", "name", "code", "description", "sort_order", "is_active")
    inlines = [DetailSegmentInline]

    @admin.display(description="Property")
    def property_name(self, obj):
        return obj.property


@admin.register(DetailSegment)
class DetailSegmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sub_segment",
        "property_name",
        "code",
        "sort_order",
        "is_active",
    )
    list_filter = ("sub_segment__segment__group__property", "is_active")
    search_fields = (
        "name",
        "code",
        "description",
        "sub_segment__name",
        "sub_segment__segment__name",
        "sub_segment__segment__group__name",
        "sub_segment__segment__group__property__name",
        "sub_segment__segment__group__property__hotel_code",
        "sub_segment__segment__group__property__resort_code",
    )
    ordering = (
        "sub_segment__segment__group__property__resort_code",
        "sub_segment__segment__group__sort_order",
        "sub_segment__segment__sort_order",
        "sub_segment__sort_order",
        "sort_order",
        "name",
    )
    fields = ("sub_segment", "name", "code", "description", "sort_order", "is_active")

    @admin.display(description="Property")
    def property_name(self, obj):
        return obj.property