from django.urls import path
from .views import (
    report_autocomplete,
    report_group_list_view,
    report_list_by_group_view,
    report_detail_view,
)

app_name = "reports"

urlpatterns = [
    path("reports/", report_group_list_view, name="group_list"),
    path("reports/<slug:slug>/", report_list_by_group_view, name="report_list"),
    path("reports/<slug:group_slug>/<slug:report_slug>/", report_detail_view, name="report_detail"),

    path("reports-search/autocomplete/", report_autocomplete, name="report_autocomplete"),
]