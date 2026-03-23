# data/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import IncomingFile, ExpectedFile


class IncomingFileListView(LoginRequiredMixin, ListView):
    model = IncomingFile
    template_name = "data/incoming_file_list.html"
    context_object_name = "files"
    paginate_by = 50

    def get_queryset(self):
        qs = IncomingFile.objects.select_related(
            "property", "source", "domain", "rule"
        ).order_by("-created_at")

        user = self.request.user

        if user.is_superuser or getattr(user, "role", None) == "super_admin":
            return qs

        if getattr(user, "role", None) == "supervisor":
            return qs.filter(property__supervisors=user)

        return qs.none()


class ExpectedFileListView(LoginRequiredMixin, ListView):
    model = ExpectedFile
    template_name = "data/expected_file_list.html"
    context_object_name = "expected_files"
    paginate_by = 50

    def get_queryset(self):
        qs = ExpectedFile.objects.select_related(
            "rule", "property", "source", "incoming_file"
        ).order_by("-expected_date", "rule__name")

        user = self.request.user

        if user.is_superuser or getattr(user, "role", None) == "super_admin":
            return qs

        if getattr(user, "role", None) == "supervisor":
            return qs.filter(property__supervisors=user)

        return qs.none()