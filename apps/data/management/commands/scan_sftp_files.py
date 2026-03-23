# data/management/commands/scan_sftp_files.py

from django.core.management.base import BaseCommand, CommandError
from data.services.scanner import scan_sources


class Command(BaseCommand):
    help = "Scan configured SFTP sources and create/update IncomingFile records."

    def add_arguments(self, parser):
        parser.add_argument("--server", type=str, help="Optional server name")
        parser.add_argument("--property", type=str, help="Optional property resort_code")
        parser.add_argument("--source", type=str, help="Optional source_name")
        parser.add_argument("--date", type=str, help="Optional file date in YYYY-MM-DD")
        parser.add_argument("--dry-run", action="store_true", help="Preview only")

    def handle(self, *args, **options):
        try:
            result = scan_sources(
                server_name=options.get("server"),
                property_code=options.get("property"),
                source_name=options.get("source"),
                file_date=options.get("date"),
                dry_run=options.get("dry_run"),
                logger=self.stdout.write,
            )
        except ValueError as exc:
            raise CommandError(str(exc))
        except Exception as exc:
            raise CommandError(f"Scan failed: {exc}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Scan complete. scanned={result['scanned']}, "
                f"created={result['created']}, "
                f"updated={result['updated']}, "
                f"dry_run={result['dry_run']}"
            )
        )


# python manage.py scan_sftp_files
# python manage.py scan_sftp_files --dry-run
# python manage.py scan_sftp_files --server main-sftp
# python manage.py scan_sftp_files --property DXB01
# python manage.py scan_sftp_files --source finance-drop
# python manage.py scan_sftp_files --date 2026-03-23