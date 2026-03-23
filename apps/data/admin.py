# data/admin.py

from django.contrib import admin
from .models import (
    FileDomain,
    SFTPServer,
    PropertySFTPSource,
    FileRule,
    IncomingFile,
    ExpectedFile,
    FileLoadBatch,
    FileLoadLog,
)


@admin.register(FileDomain)
class FileDomainAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code", "description")
    ordering = ("name",)


@admin.register(SFTPServer)
class SFTPServerAdmin(admin.ModelAdmin):
    list_display = ("name", "host", "port", "username", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "host", "username", "base_path")


@admin.register(PropertySFTPSource)
class PropertySFTPSourceAdmin(admin.ModelAdmin):
    list_display = ("property", "source_name", "server", "remote_path", "is_active")
    list_filter = ("is_active", "server")
    search_fields = ("property__name", "property__resort_code", "source_name", "remote_path")
    autocomplete_fields = ("property", "server")


@admin.register(FileRule)
class FileRuleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "property",
        "source",
        "domain",
        "match_type",
        "frequency",
        "is_required",
        "recursive_scan",
        "is_active",
    )
    list_filter = (
        "match_type",
        "frequency",
        "is_required",
        "recursive_scan",
        "is_active",
        "domain",
    )
    search_fields = (
        "name",
        "property__name",
        "property__resort_code",
        "source__source_name",
        "domain__name",
        "expected_filename_pattern",
    )
    autocomplete_fields = ("property", "source", "domain")


@admin.register(IncomingFile)
class IncomingFileAdmin(admin.ModelAdmin):
    list_display = ("file_name", "property", "source", "domain", "file_date", "status")
    list_filter = ("status", "domain", "property")
    search_fields = (
        "file_name",
        "file_path",
        "property__name",
        "property__resort_code",
        "source__source_name",
        "domain__name",
    )
    autocomplete_fields = ("property", "source", "domain", "rule")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_superuser or getattr(user, "role", None) == "super_admin":
            return qs

        if getattr(user, "role", None) == "supervisor":
            return qs.filter(property__supervisors=user)

        return qs.none()


@admin.register(ExpectedFile)
class ExpectedFileAdmin(admin.ModelAdmin):
    list_display = ("rule", "property", "source", "expected_date", "status", "is_found")
    list_filter = ("status", "is_found", "expected_date")
    search_fields = (
        "rule__name",
        "property__name",
        "property__resort_code",
        "source__source_name",
        "expected_filename",
    )
    autocomplete_fields = ("rule", "property", "source", "incoming_file")


@admin.register(FileLoadBatch)
class FileLoadBatchAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "domain",
        "source",
        "run_date",
        "status",
        "total_files",
        "loaded_files",
        "failed_files",
        "started_at",
        "completed_at",
    )
    list_filter = ("status", "run_date", "domain")
    search_fields = (
        "property__name",
        "property__resort_code",
        "domain__name",
        "source__source_name",
    )
    autocomplete_fields = ("property", "domain", "source")


@admin.register(FileLoadLog)
class FileLoadLogAdmin(admin.ModelAdmin):
    list_display = ("incoming_file", "action", "performed_by", "created_at")
    list_filter = ("action", "created_at")
    search_fields = (
        "incoming_file__file_name",
        "message",
        "performed_by__email",
    )
    autocomplete_fields = ("incoming_file", "batch", "performed_by")
    readonly_fields = ("created_at", "updated_at")