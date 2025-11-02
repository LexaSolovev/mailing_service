from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Client
from .forms import ClientForm


class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    template_name = "clients/client_detail.html"


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("clients:list")
