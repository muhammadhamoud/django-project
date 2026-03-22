from django.contrib import admin
from .models import ReportGroup, Report


@admin.register(ReportGroup)
class ReportGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "key", "slug", "is_active", "sort_order", "property_list", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "key", "description", "slug")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("allowed_properties",)

    def property_list(self, obj):
        return ", ".join(obj.allowed_properties.values_list("name", flat=True))
    property_list.short_description = "Allowed Properties"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "group",
        "key",
        "powerbi_report_id",
        "is_active",
        "sort_order",
        "property_list",
        "created_at",
    )
    list_filter = ("is_active", "group")
    search_fields = ("title", "key", "description", "slug", "powerbi_report_id")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("allowed_properties",)

    def property_list(self, obj):
        return ", ".join(obj.allowed_properties.values_list("name", flat=True))
    property_list.short_description = "Allowed Properties"