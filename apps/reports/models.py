from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)

    image = models.ImageField(upload_to="reports/images/", blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["sort_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            model_class = self.__class__
            counter = 1

            while model_class.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class ReportGroup(BaseModel):
    allowed_properties = models.ManyToManyField(
        "properties.Property",
        blank=True,
        related_name="report_groups"
    )

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "Report Group"
        verbose_name_plural = "Report Groups"

    def __str__(self):
        return self.title

    def is_accessible_by_property(self, property_obj):
        if not property_obj:
            return False

        if not self.allowed_properties.exists():
            return True

        return self.allowed_properties.filter(id=property_obj.id).exists()


class Report(BaseModel):
    group = models.ForeignKey(
        ReportGroup,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    allowed_properties = models.ManyToManyField(
        "properties.Property",
        blank=True,
        related_name="reports"
    )

    powerbi_report_id = models.CharField(max_length=255, unique=True)
    powerbi_workspace_id = models.CharField(max_length=255, blank=True, null=True)
    powerbi_embed_url = models.URLField(blank=True, null=True)
    powerbi_url = models.URLField(blank=True, null=True)
    powerbi_dataset_id = models.CharField(max_length=255, blank=True, null=True)
    powerbi_page_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return self.title

    def is_accessible_by_property(self, property_obj):
        if not property_obj:
            return False

        if not self.group.is_accessible_by_property(property_obj):
            return False

        if not self.allowed_properties.exists():
            return True

        return self.allowed_properties.filter(id=property_obj.id).exists()