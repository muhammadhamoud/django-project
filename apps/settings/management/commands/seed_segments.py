from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from properties.models import Property
from settings.models import SegmentGroup, SegmentCategory, Segment


SEGMENT_DATA = [
    {"segment_code": "CMP", "category_code": "CMP", "segment_group_code": "COM", "segment": "Complimentary", "segmentcategory": "Complimentary", "segmentgroup": "Complimentary"},
    {"segment_code": "HUS", "category_code": "CMP", "segment_group_code": "COM", "segment": "House Use", "segmentcategory": "Complimentary", "segmentgroup": "Complimentary"},
    {"segment_code": "CON", "category_code": "CON", "segment_group_code": "CON", "segment": "Contract", "segmentcategory": "Contract", "segmentgroup": "Contract"},
    {"segment_code": "GTH", "category_code": "GTH", "segment_group_code": "GRP", "segment": "Group Others", "segmentcategory": "Group Others", "segmentgroup": "Group"},
    {"segment_code": "GCO", "category_code": "GCO", "segment_group_code": "GRP", "segment": "Group Corporate", "segmentcategory": "Group Corporate", "segmentgroup": "Group"},
    {"segment_code": "GWH", "category_code": "GWH", "segment_group_code": "GRP", "segment": "Group Tour/Wholesale/Series", "segmentcategory": "Group Leisure", "segmentgroup": "Group"},
    {"segment_code": "NON", "category_code": "NON", "segment_group_code": "NON", "segment": "Non-Revenue", "segmentcategory": "Other Zero Revenue", "segmentgroup": "Non-Revenue"},
    {"segment_code": "OTH", "category_code": "OTH", "segment_group_code": "NON", "segment": "Other Revenue", "segmentcategory": "Zero Revenue", "segmentgroup": "Non-Revenue"},
    {"segment_code": "DISD", "category_code": "DIS", "segment_group_code": "TRA", "segment": "Discount Deep > 20%", "segmentcategory": "Retail Discount", "segmentgroup": "Transient"},
    {"segment_code": "DISM", "category_code": "DIS", "segment_group_code": "TRA", "segment": "Discount Medium < 20%", "segmentcategory": "Retail Discount", "segmentgroup": "Transient"},
    {"segment_code": "GOV", "category_code": "GOV", "segment_group_code": "TRA", "segment": "Government", "segmentcategory": "Negotiated", "segmentgroup": "Transient"},
    {"segment_code": "NEGL", "category_code": "NEG", "segment_group_code": "TRA", "segment": "Negotiated Global (LRA)", "segmentcategory": "Negotiated", "segmentgroup": "Transient"},
    {"segment_code": "NEGN", "category_code": "NEG", "segment_group_code": "TRA", "segment": "Negotiated Global (NLRA)", "segmentcategory": "Negotiated", "segmentgroup": "Transient"},
    {"segment_code": "NELL", "category_code": "NEG", "segment_group_code": "TRA", "segment": "Negotiated Local (LRA)", "segmentcategory": "Negotiated", "segmentgroup": "Transient"},
    {"segment_code": "NELN", "category_code": "NEG", "segment_group_code": "TRA", "segment": "Negotiated Local (NLRA)", "segmentcategory": "Negotiated", "segmentgroup": "Transient"},
    {"segment_code": "NECON", "category_code": "NEG", "segment_group_code": "TRA", "segment": "Negotiated Long Stayer", "segmentcategory": "Negotiated", "segmentgroup": "Transient"},
    {"segment_code": "ODC", "category_code": "ODC", "segment_group_code": "TRA", "segment": "Other Discount", "segmentcategory": "Other Discount", "segmentgroup": "Transient"},
    {"segment_code": "EMP", "category_code": "ODC", "segment_group_code": "TRA", "segment": "Employees/Friends/Family", "segmentcategory": "Other Discount", "segmentgroup": "Transient"},
    {"segment_code": "LOY", "category_code": "LOY", "segment_group_code": "TRA", "segment": "Loyalty", "segmentcategory": "Other Discount", "segmentgroup": "Transient"},
    {"segment_code": "PKG", "category_code": "PKG", "segment_group_code": "TRA", "segment": "Value Added Packages", "segmentcategory": "Packages", "segmentgroup": "Transient"},
    {"segment_code": "ADP", "category_code": "ADP", "segment_group_code": "TRA", "segment": "Advance Purchase", "segmentcategory": "Advance Purchase", "segmentgroup": "Transient"},
    {"segment_code": "QUA", "category_code": "QUA", "segment_group_code": "TRA", "segment": "Qualified Others", "segmentcategory": "Qualified", "segmentgroup": "Transient"},
    {"segment_code": "TFG", "category_code": "TFG", "segment_group_code": "TRA", "segment": "The First Group", "segmentcategory": "Qualified", "segmentgroup": "Transient"},
    {"segment_code": "BEN", "category_code": "BEN", "segment_group_code": "TRA", "segment": "Best Flexible Rate", "segmentcategory": "Retail", "segmentgroup": "Transient"},
    {"segment_code": "WHD", "category_code": "WHO", "segment_group_code": "TRA", "segment": "Wholesale Dynamic", "segmentcategory": "Wholesale", "segmentgroup": "Transient"},
    {"segment_code": "WHO", "category_code": "WHO", "segment_group_code": "TRA", "segment": "Wholesale Static", "segmentcategory": "Wholesale", "segmentgroup": "Transient"},
    {"segment_code": "UKN", "category_code": "UKN", "segment_group_code": "UKN", "segment": "Unknown", "segmentcategory": "Unknown", "segmentgroup": "Unknown"},
    {"segment_code": "CAT", "category_code": "CAT", "segment_group_code": "CAT", "segment": "Catering", "segmentcategory": "Catering", "segmentgroup": "Catering"},
]


class Command(BaseCommand):
    help = "Seed segment groups, categories, and segments for a property"

    def add_arguments(self, parser):
        parser.add_argument(
            "--property-code",
            required=True,
            help="Property resort_code",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing segment groups, categories, and segments for the selected property before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        property_code = options["property_code"]
        flush = options["flush"]

        try:
            property_obj = Property.objects.get(resort_code=property_code)
        except Property.DoesNotExist:
            raise CommandError(
                f"Property with resort_code '{property_code}' does not exist."
            )

        if flush:
            self._flush_property_data(property_obj)

        group_sort, category_sort, segment_sort = self._build_sort_maps()

        groups = self._seed_groups(property_obj, group_sort)
        categories = self._seed_categories(groups, category_sort)
        self._seed_segments(categories, segment_sort)

        self.stdout.write(
            self.style.SUCCESS(
                f"Segments seeded successfully for property '{property_code}'"
            )
        )

    def _flush_property_data(self, property_obj):
        self.stdout.write(
            self.style.WARNING(
                f"Flushing segment data for property '{property_obj.resort_code}'..."
            )
        )

        segments_deleted, _ = Segment.objects.filter(
            category__group__property=property_obj
        ).delete()

        categories_deleted, _ = SegmentCategory.objects.filter(
            group__property=property_obj
        ).delete()

        groups_deleted, _ = SegmentGroup.objects.filter(
            property=property_obj
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Flush complete "
                f"(segments={segments_deleted}, categories={categories_deleted}, groups={groups_deleted})"
            )
        )

    def _build_sort_maps(self):
        group_sort = {}
        category_sort = {}
        segment_sort = {}

        group_counter = 1
        category_counter = 1
        segment_counter = 1

        for row in SEGMENT_DATA:
            group_key = row["segment_group_code"]
            if group_key not in group_sort:
                group_sort[group_key] = group_counter
                group_counter += 1

            category_key = (row["segment_group_code"], row["category_code"])
            if category_key not in category_sort:
                category_sort[category_key] = category_counter
                category_counter += 1

            segment_key = (
                row["segment_group_code"],
                row["category_code"],
                row["segment_code"],
            )
            if segment_key not in segment_sort:
                segment_sort[segment_key] = segment_counter
                segment_counter += 1

        return group_sort, category_sort, segment_sort

    def _seed_groups(self, property_obj, group_sort):
        groups = {}
        seen_groups = set()

        for row in SEGMENT_DATA:
            group_code = row["segment_group_code"]

            if group_code in seen_groups:
                continue
            seen_groups.add(group_code)

            group_obj, created = SegmentGroup.objects.update_or_create(
                property=property_obj,
                code=group_code,
                defaults={
                    "name": row["segmentgroup"].strip(),
                    "sort_order": group_sort[group_code],
                },
            )
            groups[group_code] = group_obj

            self.stdout.write(
                f"{'Created' if created else 'Updated'} SegmentGroup: "
                f"{group_obj.code} - {group_obj.name}"
            )

        return groups

    def _seed_categories(self, groups, category_sort):
        categories = {}
        seen_categories = set()

        for row in SEGMENT_DATA:
            category_key = (row["segment_group_code"], row["category_code"])

            if category_key in seen_categories:
                continue
            seen_categories.add(category_key)

            category_obj, created = SegmentCategory.objects.update_or_create(
                group=groups[row["segment_group_code"]],
                code=row["category_code"],
                defaults={
                    "name": row["segmentcategory"].strip(),
                    "sort_order": category_sort[category_key],
                },
            )
            categories[category_key] = category_obj

            self.stdout.write(
                f"{'Created' if created else 'Updated'} SegmentCategory: "
                f"{category_obj.code} - {category_obj.name}"
            )

        return categories

    def _seed_segments(self, categories, segment_sort):
        for row in SEGMENT_DATA:
            category_key = (row["segment_group_code"], row["category_code"])
            segment_key = (
                row["segment_group_code"],
                row["category_code"],
                row["segment_code"],
            )

            segment_obj, created = Segment.objects.update_or_create(
                category=categories[category_key],
                code=row["segment_code"],
                defaults={
                    "name": row["segment"].strip(),
                    "sort_order": segment_sort[segment_key],
                },
            )

            self.stdout.write(
                f"{'Created' if created else 'Updated'} Segment: "
                f"{segment_obj.code} - {segment_obj.name}"
            )


# python manage.py seed_segments --property-code DEMO-RESORT-001
# python manage.py seed_segments --property-code DEMO-RESORT-001 --flush