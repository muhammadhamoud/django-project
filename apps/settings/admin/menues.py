# from django.contrib import admin
# from .models import SettingsMenu


# @admin.register(SettingsMenu)
# class SettingsMenuAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "key",
#         "slug",
#         "sort_order",
#         "is_active",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("is_active", "created_at", "updated_at")
#     search_fields = ("title", "key", "slug", "description")
#     prepopulated_fields = {"slug": ("title",)}
#     filter_horizontal = ("allowed_properties",)
#     ordering = ("sort_order", "title")
#     list_editable = ("sort_order", "is_active")
#     readonly_fields = ("created_at", "updated_at")

#     fieldsets = (
#         ("Basic Info", {
#             "fields": ("title", "slug", "key", "description")
#         }),
#         ("Display", {
#             "fields": ("icon", "color", "image", "sort_order", "is_active")
#         }),
#         ("Access Control", {
#             "fields": ("allowed_properties",)
#         }),
#         ("Timestamps", {
#             "fields": ("created_at", "updated_at")
#         }),
#     )

from django.contrib import admin
from settings.models import SettingsMenu


@admin.register(SettingsMenu)
class SettingsMenuAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "key",
        "slug",
        "sort_order",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("title", "key", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("allowed_properties",)
    ordering = ("sort_order", "title")
    list_editable = ("sort_order", "is_active")
    readonly_fields = ("created_at", "updated_at")
    actions = ("make_active", "make_inactive")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "key", "description")
        }),
        ("Display", {
            "fields": ("icon", "color", "image", "sort_order", "is_active")
        }),
        ("Access Control", {
            "fields": ("allowed_properties",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

    @admin.action(description="Mark selected menus as active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected menus as inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)