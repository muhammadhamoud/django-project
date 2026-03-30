import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.text import Truncator

from .models import Subscriber, Contact


# @admin.register(Subscriber)
# class SubscriberAdmin(admin.ModelAdmin):
#     list_display = ("email", "is_subscribed", "created_at", "updated_at")
#     list_filter = ("is_subscribed", "created_at", "updated_at")
#     search_fields = ("email",)
#     ordering = ("-created_at",)
#     list_per_page = 25


@admin.action(description="Mark selected messages as handled")
def mark_as_handled(modeladmin, request, queryset):
    updated = queryset.update(action=True)
    modeladmin.message_user(
        request,
        f"{updated} message(s) marked as handled.",
        level=messages.SUCCESS,
    )


@admin.action(description="Mark selected messages as pending")
def mark_as_pending(modeladmin, request, queryset):
    updated = queryset.update(action=False)
    modeladmin.message_user(
        request,
        f"{updated} message(s) marked as pending.",
        level=messages.SUCCESS,
    )


@admin.action(description="Export selected contacts to CSV")
def export_contacts_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contacts_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "ID",
        "Name",
        "Email",
        "Phone",
        "Subject",
        "Message",
        "Action",
        "Submission Date",
        "IP Address",
        "User Agent",
    ])

    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.name,
            obj.email,
            obj.phone,
            obj.subject,
            obj.message,
            "Handled" if obj.action else "Pending",
            obj.submission_date.strftime("%Y-%m-%d %H:%M:%S") if obj.submission_date else "",
            obj.ip_address or "",
            obj.user_agent or "",
        ])

    return response


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email_link",
        "phone_link",
        "short_subject",
        "status_badge",
        "short_message",
        "submission_date",
        "ip_address",
    )
    list_display_links = ("id", "name")
    list_filter = ("action", "submission_date")
    search_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "ip_address",
        "user_agent",
    )
    readonly_fields = (
        "submission_date",
        "ip_address",
        "user_agent",
        "message_preview",
    )
    ordering = ("-submission_date",)
    date_hierarchy = "submission_date"
    list_per_page = 25
    actions = (mark_as_handled, mark_as_pending, export_contacts_csv)

    fieldsets = (
        ("Contact Information", {
            "fields": (
                "name",
                "email",
                "phone",
                "subject",
                "message",
                "message_preview",
            )
        }),
        ("Status", {
            "fields": (
                "action",
                "submission_date",
            )
        }),
        ("Technical Details", {
            "classes": ("collapse",),
            "fields": (
                "ip_address",
                "user_agent",
            )
        }),
    )

    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_link.short_description = "Email"
    email_link.admin_order_field = "email"

    def phone_link(self, obj):
        if not obj.phone:
            return "-"
        return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)
    phone_link.short_description = "Phone"
    phone_link.admin_order_field = "phone"

    def short_subject(self, obj):
        return Truncator(obj.subject).chars(40)
    short_subject.short_description = "Subject"
    short_subject.admin_order_field = "subject"

    def short_message(self, obj):
        return Truncator(obj.message).chars(60)
    short_message.short_description = "Message"

    def status_badge(self, obj):
        if obj.action:
            return format_html(
                '<span style="padding:4px 10px;border-radius:999px;background:#dcfce7;color:#166534;font-weight:600;">{}</span>',
                "Handled"
            )
        return format_html(
            '<span style="padding:4px 10px;border-radius:999px;background:#fee2e2;color:#991b1b;font-weight:600;">{}</span>',
            "Pending"
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = "action"

    def message_preview(self, obj):
        if not obj.message:
            return "-"
        return format_html(
            "<div style='max-width:720px; white-space:pre-wrap; line-height:1.6;'>{}</div>",
            obj.message,
        )
    message_preview.short_description = "Full Message"



@admin.action(description="Mark selected emails as subscribed")
def mark_as_subscribed(modeladmin, request, queryset):
    updated = queryset.update(is_subscribed=True)
    modeladmin.message_user(
        request,
        f"{updated} subscriber(s) marked as subscribed.",
        level=messages.SUCCESS,
    )


@admin.action(description="Mark selected emails as unsubscribed")
def mark_as_unsubscribed(modeladmin, request, queryset):
    updated = queryset.update(is_subscribed=False)
    modeladmin.message_user(
        request,
        f"{updated} subscriber(s) marked as unsubscribed.",
        level=messages.SUCCESS,
    )


@admin.action(description="Export selected subscribers to CSV")
def export_subscribers_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="subscribers_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Email", "Subscribed", "Created At", "Updated At"])

    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.email,
            "Yes" if obj.is_subscribed else "No",
            obj.created_at.strftime("%Y-%m-%d %H:%M:%S") if obj.created_at else "",
            obj.updated_at.strftime("%Y-%m-%d %H:%M:%S") if obj.updated_at else "",
        ])

    return response


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_subscribed", "created_at", "updated_at")
    list_filter = ("is_subscribed", "created_at", "updated_at")
    search_fields = ("email",)
    ordering = ("-created_at",)
    list_per_page = 25
    actions = (mark_as_subscribed, mark_as_unsubscribed, export_subscribers_csv)


