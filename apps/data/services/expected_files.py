# data/services/expected_files.py

from django.utils import timezone
from data.models import FileRule, ExpectedFile


def should_generate_for_date(rule, target_date):
    if rule.frequency == "daily":
        return True

    if rule.frequency == "weekly":
        return target_date.weekday() == 0

    if rule.frequency == "monthly":
        return target_date.day == 1

    return False


def generate_expected_files(target_date=None):
    target_date = target_date or timezone.localdate()

    rules = FileRule.objects.filter(
        is_active=True,
        is_required=True,
        property__is_active=True,
        source__is_active=True,
    ).select_related("property", "source")

    created_count = 0

    for rule in rules:
        if not should_generate_for_date(rule, target_date):
            continue

        _, created = ExpectedFile.objects.get_or_create(
            rule=rule,
            expected_date=target_date,
            defaults={
                "property": rule.property,
                "source": rule.source,
                "expected_filename": rule.expected_filename_pattern,
                "status": ExpectedFile.Status.PENDING,
            },
        )

        if created:
            created_count += 1

    return created_count


def mark_expected_file_found(rule, file_date, incoming_file):
    if not rule or not file_date:
        return

    ExpectedFile.objects.filter(
        rule=rule,
        expected_date=file_date,
    ).update(
        is_found=True,
        status=ExpectedFile.Status.FOUND,
        found_at=timezone.now(),
        incoming_file=incoming_file,
    )


def mark_missing_or_late_expected_files():
    now = timezone.localtime()
    today = now.date()

    pending_items = ExpectedFile.objects.filter(
        status=ExpectedFile.Status.PENDING,
        rule__is_required=True,
        expected_date__lte=today,
    ).select_related("rule")

    updated_count = 0

    for item in pending_items:
        expected_by_time = item.rule.expected_by_time

        if item.expected_date < today:
            item.status = ExpectedFile.Status.MISSING
            item.note = "Expected date passed and no file was found."
            item.save(update_fields=["status", "note", "updated_at"])
            updated_count += 1
            continue

        if item.expected_date == today and expected_by_time and now.time() > expected_by_time:
            item.status = ExpectedFile.Status.LATE
            item.note = "Expected time passed and file has not been found yet."
            item.save(update_fields=["status", "note", "updated_at"])
            updated_count += 1

    return updated_count