# data/tasks.py

from celery import shared_task
from django.utils import timezone

from data.services.expected_files import (
    generate_expected_files,
    mark_missing_or_late_expected_files,
)
from data.services.scanner import scan_sources


@shared_task
def generate_expected_files_task():
    return generate_expected_files(target_date=timezone.localdate())


@shared_task
def scan_sftp_sources_task(server_name=None, property_code=None, source_name=None, file_date=None):
    return scan_sources(
        server_name=server_name,
        property_code=property_code,
        source_name=source_name,
        file_date=file_date,
        dry_run=False,
    )


@shared_task
def mark_missing_or_late_expected_files_task():
    return mark_missing_or_late_expected_files()


# dd to your Celery config:

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "generate-expected-files-daily": {
        "task": "data.tasks.generate_expected_files_task",
        "schedule": crontab(hour=0, minute=5),
    },
    "scan-sftp-every-30-minutes": {
        "task": "data.tasks.scan_sftp_sources_task",
        "schedule": crontab(minute="*/30"),
    },
    "mark-missing-files-every-hour": {
        "task": "data.tasks.mark_missing_or_late_expected_files_task",
        "schedule": crontab(minute=0),
    },
}