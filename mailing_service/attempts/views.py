from django.views.generic import ListView, DetailView
from .models import Attempt
from django.contrib.auth.mixins import LoginRequiredMixin


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "attempts/attempt_list.html"
    context_object_name = "attempts"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(mailing__owner=self.request.user)
        return queryset.select_related("mailing", "client")


class AttemptDetailView(LoginRequiredMixin, DetailView):
    model = Attempt
    template_name = "attempts/attempt_detail.html"
    context_object_name = "attempt"

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(mailing__owner=self.request.user)
        return queryset.select_related("mailing", "client")
