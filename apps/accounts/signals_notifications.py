from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import NotificationRecipient
from .models import Notification

User = get_user_model()


def create_notification_for_users(title, message, users, created_by=None, level="info", link=None):
    notification = Notification.objects.create(
        title=title,
        message=message,
        level=level,
        link=link,
        created_by=created_by,
    )

    NotificationRecipient.objects.bulk_create(
        [
            NotificationRecipient(notification=notification, user=user)
            for user in users
        ],
        ignore_conflicts=True,
    )
    return notification


@receiver(post_save, sender=User)
def notify_admins_when_user_created(sender, instance, created, **kwargs):
    if not created:
        return

    # Safety: make sure the profile exists
    profile = getattr(instance, "profile", None)
    if not profile:
        return

    user_property_ids = profile.properties.values_list("id", flat=True)

    if not user_property_ids:
        return

    admins = User.objects.filter(
        is_active=True,
        profile__roles__code__in=["super_admin", "supervisor", "admin"],
        profile__properties__id__in=user_property_ids,
    ).exclude(
        id=instance.id
    ).distinct()

    if admins.exists():
        create_notification_for_users(
            title="New user registered",
            message=f"{instance.first_name} {instance.last_name} ({instance.email}) has created an account.",
            users=admins,
            level="info",
            alert=False,
            link="/accounts/users/",
        )