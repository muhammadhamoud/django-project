from django.db import models


class Property(models.Model):
    hotel_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique property code in multi-property operations."
    )
    resort_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique property code in multi-property operations."
    )
    name = models.CharField(max_length=150, blank=True)

    begin_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the property becomes active."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the property is no longer active."
    )

    chain_mode = models.CharField(
        max_length=50,
        blank=True,
        help_text="Read-only chain mode."
    )
    country_mode = models.CharField(
        max_length=50,
        blank=True,
        help_text="Country-specific business logic mode."
    )

    currency = models.CharField(max_length=10, blank=True)
    currency_format = models.CharField(max_length=50, blank=True)

    catering_currency = models.CharField(max_length=10, blank=True)
    catering_currency_format = models.CharField(max_length=50, blank=True)

    short_date_format = models.CharField(max_length=30, blank=True)
    long_date_format = models.CharField(max_length=50, blank=True)
    time_format = models.CharField(max_length=30, blank=True)
    time_zone = models.CharField(max_length=64, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["hotel_code"]

    def __str__(self):
        return f"{self.hotel_code} - {self.name}" if self.name else self.hotel_code



    

