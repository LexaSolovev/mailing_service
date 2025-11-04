from django.db import models
from users.models import User


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        permissions = [
            ("can_view_all_clients", "Может просматривать всех клиентов"),
            ("can_block_client", "Может блокировать клиентов"),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.email})"
