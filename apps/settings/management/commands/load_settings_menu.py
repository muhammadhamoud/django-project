import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from settings.models import SettingsMenu

# python manage.py load_settings_menu
# python manage.py load_settings_menu --flush
# python manage.py load_settings_menu --update
# python manage.py load_settings_menu --flush --update


FIXTURE_DATA = [
    {
        "title": "Market segmentation",
        "key": "market_segment",
        "description": "Group guests and bookings into meaningful segments to better understand demand patterns and guest behavior.",
        "sort_order": 1,
        "color": "amber",
        "icon": "fa-solid fa-people-group",
    },
    {
        "title": "Room type",
        "key": "room_type",
        "description": "Define room categories and pricing relationships to keep your inventory structured and easy to analyze.",
        "sort_order": 2,
        "color": "blue",
        "icon": "fa-solid fa-bed",
    },
    {
        "title": "Package",
        "key": "package",
        "description": "Organize packages into clear groups so you can measure which offers drive the most bookings and revenue.",
        "sort_order": 3,
        "color": "emerald",
        "icon": "fa-solid fa-box-open",
    },
    {
        "title": "Rate code",
        "key": "rate_code",
        "description": "Structure rate codes into meaningful groups to track performance and identify your most effective pricing strategies.",
        "sort_order": 4,
        "color": "emerald",
        "icon": "fa-solid fa-tags",
    },
    {
        "title": "Travel agent",
        "key": "travel_agent",
        "description": "Organize travel agents to evaluate performance, strengthen partnerships, and uncover new business opportunities.",
        "sort_order": 5,
        "color": "cyan",
        "icon": "fa-solid fa-plane-departure",
    },
    {
        "title": "Guest country",
        "key": "guest_country",
        "description": "See where your guests are coming from so you can refine marketing efforts and attract the right audiences.",
        "sort_order": 6,
        "color": "rose",
        "icon": "fa-solid fa-earth-americas",
    },
    {
        "title": "Company",
        "key": "company",
        "description": "Classify reservations by company to support corporate account management and grow your business segment.",
        "sort_order": 7,
        "color": "violet",
        "icon": "fa-solid fa-building",
    },
    {
        "title": "Day of week",
        "key": "day_of_week",
        "description": "Create weekday and weekend groupings that match your business logic for clearer demand analysis.",
        "sort_order": 8,
        "color": "orange",
        "icon": "fa-solid fa-calendar-days",
    },
    {
        "title": "Booking Source",
        "key": "booking_source",
        "description": "Organize booking channels like direct, wholesale, and OTA sources to sharpen your distribution insights.",
        "sort_order": 9,
        "color": "sky",
        "icon": "fa-solid fa-share-nodes",
    },
    {
        "title": "Origin",
        "key": "origin",
        "description": "Map reservation origins such as websites and channel managers to improve visibility across your booking journey.",
        "sort_order": 10,
        "color": "teal",
        "icon": "fa-solid fa-location-dot",
    },
    {
        "title": "Competitor",
        "key": "competitor",
        "description": "Set up competitor groups to simplify rate benchmarking and support smarter pricing decisions.",
        "sort_order": 11,
        "color": "indigo",
        "icon": "fa-solid fa-door-open",
    },
    {
        "title": "Loyalty",
        "key": "loyalty",
        "description": "Organize loyalty data into meaningful tiers or groups so you can better understand member value and engagement.",
        "sort_order": 12,
        "color": "pink",
        "icon": "fa-solid fa-award",
    },
]
class Command(BaseCommand):
    help = "Load default SettingsMenu data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing SettingsMenu records before loading",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing records matched by key instead of skipping them",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        flush = options["flush"]
        update = options["update"]

        if flush:
            deleted_count, _ = SettingsMenu.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing records."))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for item in FIXTURE_DATA:
            obj = SettingsMenu.objects.filter(key=item["key"]).first()

            if obj:
                if update:
                    obj.title = item["title"]
                    obj.description = item["description"]
                    obj.sort_order = item["sort_order"]
                    obj.color = item.get("color")
                    obj.icon = item.get("icon")
                    obj.is_active = True
                    obj.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated: {obj.title}"))
                else:
                    skipped_count += 1
                    self.stdout.write(f"Skipped existing: {obj.title}")
                continue

            SettingsMenu.objects.create(
                title=item["title"],
                key=item["key"],
                description=item["description"],
                sort_order=item["sort_order"],
                color=item.get("color"),
                icon=item.get("icon"),
                is_active=True,
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created: {item['title']}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Settings menu load completed."))
        self.stdout.write(f"Created: {created_count}")
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")