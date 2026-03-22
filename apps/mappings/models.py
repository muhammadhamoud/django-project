from django.db import models
from properties.models import Property

class BaseModel(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True, null=True)
    description =  models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)
    

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
        unique_together = [("property", "name"), ("property", "code")]


class Segment(BaseModel):
    group = models.ForeignKey(
        SegmentGroup,
        on_delete=models.CASCADE,
        related_name="segments",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "segment"
        ordering = ["sort_order", "name"]
        unique_together = [("group", "name"), ("group", "code")]

    @property
    def property(self):
        return self.group.property


class SubSegment(BaseModel):
    segment = models.ForeignKey(
        Segment,
        on_delete=models.CASCADE,
        related_name="sub_segments",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "sub_segment"
        ordering = ["sort_order", "name"]
        unique_together = [("segment", "name"), ("segment", "code")]

    @property
    def property(self):
        return self.segment.property


class DetailSegment(BaseModel):
    sub_segment = models.ForeignKey(
        SubSegment,
        on_delete=models.CASCADE,
        related_name="detail_segments",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "detail_segment"
        ordering = ["sort_order", "name"]
        unique_together = [("sub_segment", "name"), ("sub_segment", "code")]

    @property
    def property(self):
        return self.sub_segment.property
    

# class SegmentCodeMapping(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     source_code = models.CharField(max_length=50)
#     source_name = models.CharField(max_length=255, blank=True, null=True)
#     segment_group = models.ForeignKey(SegmentGroup, null=True, blank=True, on_delete=models.SET_NULL)
#     segment = models.ForeignKey(Segment, null=True, blank=True, on_delete=models.SET_NULL)
#     sub_segment = models.ForeignKey(SubSegment, null=True, blank=True, on_delete=models.SET_NULL)
#     detail_segment = models.ForeignKey(DetailSegment, null=True, blank=True, on_delete=models.SET_NULL)
#     is_active = models.BooleanField(default=True)