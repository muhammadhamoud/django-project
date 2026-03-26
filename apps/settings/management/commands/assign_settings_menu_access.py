# python manage.py assign_settings_menu_access --all-settings-menus --all-properties
# python manage.py assign_settings_menu_access --all-settings-menus --resort-codes DXB01 AUH02
# python manage.py assign_settings_menu_access --settings-menu market-segmentation --all-properties
# python manage.py assign_settings_menu_access --settings-menu market-segmentation --resort-codes DXB01 AUH02
# python manage.py assign_settings_menu_access --settings-menu market-segmentation --resort-codes DXB01 --clear-existing

# python manage.py assign_settings_menu_access --all-settings-menus --all-properties
# python manage.py assign_settings_menu_access --all-settings-menus --resort-codes DXB01 AUH02
# python manage.py assign_settings_menu_access --settings-menu market-segmentation --all-properties
# python manage.py assign_settings_menu_access --settings-menu market-segmentation --resort-codes DXB01 AUH02

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from settings.models import SettingsMenu
from properties.models import Property


class Command(BaseCommand):
    help = "Assign settings menu access to all properties or selected properties."

    def add_arguments(self, parser):
        parser.add_argument(
            "--settings-menu",
            help="Specific settings menu identifier: slug, key, or title.",
        )
        parser.add_argument(
            "--all-settings-menus",
            action="store_true",
            help="Apply to all settings menus.",
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
        settings_menu_identifier = options.get("settings_menu")
        all_settings_menus = options.get("all_settings_menus")
        all_properties = options.get("all_properties")
        resort_codes = options.get("resort_codes") or []
        clear_existing = options.get("clear_existing")

        target_count = sum([
            1 if settings_menu_identifier else 0,
            1 if all_settings_menus else 0,
        ])

        if target_count != 1:
            raise CommandError(
                "Choose exactly one target: --settings-menu or --all-settings-menus."
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
            settings_menus = self.get_settings_menus(
                all_settings_menus=all_settings_menus,
                identifier=settings_menu_identifier,
            )

            for settings_menu in settings_menus:
                if clear_existing:
                    settings_menu.allowed_properties.clear()
                settings_menu.allowed_properties.add(*properties)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Assigned {settings_menus.count()} settings menu(s) to {properties.count()} propert(ies)."
                )
            )
            self.stdout.write(
                f"Settings Menus: {', '.join(settings_menus.values_list('title', flat=True)[:10])}"
                + (" ..." if settings_menus.count() > 10 else "")
            )

        self.stdout.write(
            f"Properties: {', '.join(properties.values_list('resort_code', flat=True)[:20])}"
            + (" ..." if properties.count() > 20 else "")
        )

    def get_settings_menus(self, all_settings_menus=False, identifier=None):
        if all_settings_menus:
            settings_menus = SettingsMenu.objects.filter(is_active=True)
            if not settings_menus.exists():
                raise CommandError("No active settings menus found.")
            return settings_menus

        settings_menu = (
            SettingsMenu.objects.filter(slug=identifier).first()
            or SettingsMenu.objects.filter(key=identifier).first()
            or SettingsMenu.objects.filter(title=identifier).first()
        )

        if not settings_menu:
            raise CommandError(
                f"Settings menu '{identifier}' not found by slug, key, or title."
            )

        return SettingsMenu.objects.filter(pk=settings_menu.pk)

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
    

# python manage.py assign_settings_menu_access --all-settings-menus --all-properties
# python manage.py assign_settings_menu_access --settings-menu market-segmentation --resort-codes DXB01 AUH02
# python manage.py assign_settings_menu_access --settings-menu market_segment --resort-codes DXB01 --clear-existing