from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        ("user", "Пользователь"),
        ("manager", "Менеджер"),
    ]

    role = models.CharField(max_length=10, choices=ROLES, default="user")
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_manager(self):
        return self.role == "manager"
