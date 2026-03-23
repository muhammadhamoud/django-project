# data/urls.py

from django.urls import path
from .views import IncomingFileListView, ExpectedFileListView

app_name = "data"

urlpatterns = [
    path("incoming-files/", IncomingFileListView.as_view(), name="incoming_file_list"),
    path("expected-files/", ExpectedFileListView.as_view(), name="expected_file_list"),
]