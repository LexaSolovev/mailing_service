from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Mailing(models.Model):
    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_COMPLETED, "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Время начала рассылки")
    end_time = models.DateTimeField(verbose_name="Время окончания рассылки")
    first_sent = models.DateTimeField(
        verbose_name="Дата первой отправки", null=True, blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        "my_messages.Message", on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField("clients.Client", verbose_name="Клиенты")
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_time"]
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_disable_mailing", "Может отключать рассылки"),
            ("can_block_mailing", "Может блокировать рассылки"),
        ]

    def __str__(self):
        return f"Рассылка #{self.id} ({self.get_status_display()})"

    def clean(self):
        # Проверка, что время окончания позже времени начала
        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания должно быть позже времени начала")

    def update_status(self):
        now = timezone.now()
        if self.status == self.STATUS_CREATED and now >= self.start_time:
            self.status = self.STATUS_STARTED
            self.save()
        elif self.status == self.STATUS_STARTED and now > self.end_time:
            self.status = self.STATUS_COMPLETED
            self.save()
        return self.status

    def save(self, *args, **kwargs):
        # При первом сохранении проверяем статус
        if not self.pk:
            self.update_status()
        super().save(*args, **kwargs)
