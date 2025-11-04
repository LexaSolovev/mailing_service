from django import forms
from .models import Mailing
from clients.models import Client
from my_messages.models import Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["clients"].queryset = Client.objects.filter(owner=user)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
