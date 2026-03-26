from django.db import models
from django.urls import reverse
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


class SettingsMenu(BaseModel):
    allowed_properties = models.ManyToManyField(
        "properties.Property",
        blank=True,
        related_name="setting_menues"
    )

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "Settings Menu"
        verbose_name_plural = "Settings Menues"

    def __str__(self):
        return self.title

    def is_accessible_by_property(self, property_obj):
        if not property_obj:
            return False

        if not self.allowed_properties.exists():
            return True

        return self.allowed_properties.filter(id=property_obj.id).exists()

    def get_absolute_url(self):
        return reverse("settings:menu_items", args=[self.slug])