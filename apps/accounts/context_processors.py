def account_ui_context(request):
    can_view_users = False

    if request.user.is_authenticated and hasattr(request.user, "profile"):
        can_view_users = request.user.profile.roles.filter(
            code__in=["super_admin", "supervisor"]
        ).exists()

    return {
        "can_view_users": can_view_users,
    }

from .models import NotificationRecipient

def notification_context(request):
    unread_notification_count = 0
    unread_notifications_preview = []

    if request.user.is_authenticated:
        qs = NotificationRecipient.objects.filter(
            user=request.user,
            is_read=False,
            notification__alert=True,
        ).select_related("notification").order_by("-created_at")
        qss = NotificationRecipient.objects.filter(
            user=request.user,
            is_read=False,
        ).select_related("notification").order_by("-created_at")

        unread_notification_count = qss.count()
        unread_notifications_preview = list(qs[:1])

    return {
        "unread_notification_count": unread_notification_count,
        "unread_notifications_preview": unread_notifications_preview,
    }

