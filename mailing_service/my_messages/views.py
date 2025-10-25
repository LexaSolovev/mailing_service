from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Message
from .forms import MessageForm

class MessageListView(ListView):
    model = Message
    template_name = 'my_messages/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'my_messages/message_form.html'
    success_url = reverse_lazy('my_messages:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MessageDetailView(DetailView):
    model = Message
    template_name = 'my_messages/message_detail.html'

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'my_messages/message_form.html'
    success_url = reverse_lazy('my_messages:list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'my_messages/message_confirm_delete.html'
    success_url = reverse_lazy('my_messages:list')