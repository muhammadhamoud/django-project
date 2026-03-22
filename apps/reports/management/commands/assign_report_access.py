
# python manage.py assign_report_access --all-reports --all-properties
# python manage.py assign_report_access --all-reports --resort-codes DXB01 AUH02
# python manage.py assign_report_access --report daily-revenue --all-properties
# python manage.py assign_report_access --report daily-revenue --resort-codes DXB01 AUH02
# python manage.py assign_report_access --all-reports --all-properties --group-too
# python manage.py assign_report_access --report daily-revenue --resort-codes DXB01 --clear-existing --group-too

# python manage.py assign_report_access --all-reports --all-properties
# python manage.py assign_report_access --all-reports --resort-codes DXB01 AUH02
# python manage.py assign_report_access --report daily-revenue --all-properties
# python manage.py assign_report_access --report daily-revenue --resort-codes DXB01 AUH02

# python manage.py assign_report_access --all-groups --all-properties
# python manage.py assign_report_access --all-groups --resort-codes DXB01 AUH02
# python manage.py assign_report_access --group revenue --all-properties
# python manage.py assign_report_access --group revenue --resort-codes DXB01 AUH02

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from reports.models import Report, ReportGroup
from properties.models import Property


class Command(BaseCommand):
    help = "Assign report or group access to all properties or selected properties."

    def add_arguments(self, parser):
        parser.add_argument(
            "--report",
            help="Specific report identifier: slug, key, or title.",
        )
        parser.add_argument(
            "--all-reports",
            action="store_true",
            help="Apply to all reports.",
        )
        parser.add_argument(
            "--group",
            help="Specific group identifier: slug, key, or title.",
        )
        parser.add_argument(
            "--all-groups",
            action="store_true",
            help="Apply to all groups.",
        )
        parser.add_argument(
            "--all-properties",
            action="store_true",
            help="Assign to all active properties.",
        )
        parser.add_argument(
            "--resort-codes",
            nargs="+",
            help="Assign to specific properties by resort_code.",
        )
        parser.add_argument(
            "--clear-existing",
            action="store_true",
            help="Clear existing property assignments before assigning new ones.",
        )

    def handle(self, *args, **options):
        report_identifier = options.get("report")
        all_reports = options.get("all_reports")
        group_identifier = options.get("group")
        all_groups = options.get("all_groups")
        all_properties = options.get("all_properties")
        resort_codes = options.get("resort_codes") or []
        clear_existing = options.get("clear_existing")

        target_count = sum([
            1 if report_identifier else 0,
            1 if all_reports else 0,
            1 if group_identifier else 0,
            1 if all_groups else 0,
        ])

        if target_count != 1:
            raise CommandError(
                "Choose exactly one target: --report, --all-reports, --group, or --all-groups."
            )

        if not all_properties and not resort_codes:
            raise CommandError("Provide either --all-properties or --resort-codes.")
        if all_properties and resort_codes:
            raise CommandError("Use either --all-properties or --resort-codes, not both.")

        properties = self.get_properties(
            all_properties=all_properties,
            resort_codes=resort_codes,
        )

        with transaction.atomic():
            if all_reports or report_identifier:
                reports = self.get_reports(
                    all_reports=all_reports,
                    identifier=report_identifier,
                )

                for report in reports:
                    if clear_existing:
                        report.allowed_properties.clear()
                    report.allowed_properties.add(*properties)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Assigned {reports.count()} report(s) to {properties.count()} propert(ies)."
                    )
                )
                self.stdout.write(
                    f"Reports: {', '.join(reports.values_list('title', flat=True)[:10])}"
                    + (" ..." if reports.count() > 10 else "")
                )

            elif all_groups or group_identifier:
                groups = self.get_groups(
                    all_groups=all_groups,
                    identifier=group_identifier,
                )

                for group in groups:
                    if clear_existing:
                        group.allowed_properties.clear()
                    group.allowed_properties.add(*properties)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Assigned {groups.count()} group(s) to {properties.count()} propert(ies)."
                    )
                )
                self.stdout.write(
                    f"Groups: {', '.join(groups.values_list('title', flat=True)[:10])}"
                    + (" ..." if groups.count() > 10 else "")
                )

        self.stdout.write(
            f"Properties: {', '.join(properties.values_list('resort_code', flat=True)[:20])}"
            + (" ..." if properties.count() > 20 else "")
        )

    def get_reports(self, all_reports=False, identifier=None):
        if all_reports:
            reports = Report.objects.filter(is_active=True).select_related("group")
            if not reports.exists():
                raise CommandError("No active reports found.")
            return reports

        report = (
            Report.objects.filter(slug=identifier).select_related("group").first()
            or Report.objects.filter(key=identifier).select_related("group").first()
            or Report.objects.filter(title=identifier).select_related("group").first()
        )

        if not report:
            raise CommandError(
                f"Report '{identifier}' not found by slug, key, or title."
            )

        return Report.objects.filter(pk=report.pk).select_related("group")

    def get_groups(self, all_groups=False, identifier=None):
        if all_groups:
            groups = ReportGroup.objects.filter(is_active=True)
            if not groups.exists():
                raise CommandError("No active report groups found.")
            return groups

        group = (
            ReportGroup.objects.filter(slug=identifier).first()
            or ReportGroup.objects.filter(key=identifier).first()
            or ReportGroup.objects.filter(title=identifier).first()
        )

        if not group:
            raise CommandError(
                f"Group '{identifier}' not found by slug, key, or title."
            )

        return ReportGroup.objects.filter(pk=group.pk)

    def get_properties(self, all_properties=False, resort_codes=None):
        if all_properties:
            properties = Property.objects.filter(is_active=True)
            if not properties.exists():
                raise CommandError("No active properties found.")
            return properties

        properties = Property.objects.filter(
            resort_code__in=resort_codes,
            is_active=True,
        )

        found_codes = set(properties.values_list("resort_code", flat=True))
        missing_codes = sorted(set(resort_codes) - found_codes)

        if missing_codes:
            raise CommandError(
                f"These resort codes were not found or inactive: {', '.join(missing_codes)}"
            )

        return properties