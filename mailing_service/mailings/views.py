from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Mailing
from .forms import MailingForm
from .services import send_mailing_service
from users.mixins import OwnerRequiredMixin


class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/list.html"

    def get_queryset(self):
        if self.request.user.is_manager:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object
        context["attempts"] = mailing.attempt_set.all().order_by("-attempt_time")[:10]
        context["success_count"] = mailing.attempt_set.filter(status="success").count()
        context["failure_count"] = mailing.attempt_set.filter(status="failure").count()
        return context


class MailingDeleteView(
    LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:list")
    success_message = "Рассылка успешно удалена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing"] = self.object
        return context


def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if not request.user.is_manager and mailing.owner != request.user:
        messages.error(request, "У вас нет прав для отправки этой рассылки")
        return redirect("mailings:detail", pk=pk)

    if mailing.status not in ["created", "started"]:
        messages.error(request, "Нельзя отправить завершенную рассылку")
        return redirect("mailings:detail", pk=pk)

    send_mailing_service(mailing)
    messages.success(request, "Рассылка успешно запущена")
    return redirect("mailings:detail", pk=pk)
