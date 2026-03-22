from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "hotel_code",
        "name",
        "country_mode",
        "currency",
        "time_zone",
        "begin_date",
        "end_date",
    )
    search_fields = ("hotel_code", "name", "country_mode", "currency", "time_zone")
    list_filter = ("country_mode", "currency", "time_zone")