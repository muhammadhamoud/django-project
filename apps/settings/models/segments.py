import builtins
from django.core.exceptions import ValidationError
from django.db import models
from .commons import BaseModel
from properties.models import Property


class SegmentGroup(BaseModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="segment_groups",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "segment_group"
        ordering = ["property__resort_code", "sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "code"],
                name="uniq_segment_group_property_code",
            ),
        ]

    def clean(self):
        super().clean()
        if not self.property_id:
            raise ValidationError({"property": "Property is required."})

    def __str__(self):
        return f"{self.property} - {self.code} - {self.name}"


class SegmentCategory(BaseModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="segment_categories",
        # null=True, blank=True,
    )
    group = models.ForeignKey(
        SegmentGroup,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Segment Category"
        verbose_name_plural = "Segment Categories"
        db_table = "segment_category"
        ordering = ["property__resort_code", "group__sort_order", "sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "code"],
                name="uniq_segment_category_property_code",
            ),
        ]

    def clean(self):
        super().clean()

        if not self.property_id:
            raise ValidationError({"property": "Property is required."})

        if self.group_id and self.group.property_id != self.property_id:
            raise ValidationError({
                "group": "Selected group must belong to the same property."
            })

    def save(self, *args, **kwargs):
        if self.group_id:
            self.property = self.group.property
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property} - {self.code} - {self.name}"


class Segment(BaseModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="segments",
        # null=True, blank=True,
    )
    group = models.ForeignKey(
        SegmentGroup,
        on_delete=models.CASCADE,
        related_name="segments",
    )
    category = models.ForeignKey(
        SegmentCategory,
        on_delete=models.CASCADE,
        related_name="segments",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "segment"
        ordering = [
            "property__resort_code",
            "group__sort_order",
            "category__sort_order",
            "sort_order",
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "code"],
                name="uniq_segment_property_code",
            ),
        ]

    def clean(self):
        super().clean()

        errors = {}

        if not self.property_id:
            errors["property"] = "Property is required."

        if self.group_id and self.group.property_id != self.property_id:
            errors["group"] = "Selected group must belong to the same property."

        if self.category_id and self.category.property_id != self.property_id:
            errors["category"] = "Selected category must belong to the same property."

        if self.category_id and self.group_id and self.category.group_id != self.group_id:
            errors["category"] = "Selected category must belong to the selected group."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.category_id:
            self.property = self.category.property
            self.group = self.category.group
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property} - {self.code} - {self.name}"


class SegmentDetail(BaseModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="segment_details",
        # null=True, blank=True,
    )
    segment = models.ForeignKey(
        Segment,
        on_delete=models.SET_NULL,
        related_name="details",
        null=True,
        blank=True,
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "segment_detail"
        ordering = ["property__resort_code", "sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "code"],
                name="uniq_segment_detail_property_code",
            ),
        ]

    def clean(self):
        super().clean()
        if self.segment_id and self.segment.property_id != self.property_id:
            raise ValidationError({
                "segment": "Selected segment must belong to the same property."
            })

    @builtins.property
    def group(self):
        return self.segment.group if self.segment else None

    @builtins.property
    def category(self):
        return self.segment.category if self.segment else None

    def __str__(self):
        return f"{self.property} - {self.code} - {self.name}"