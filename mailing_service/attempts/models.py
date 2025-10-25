from django.db import models
from django.urls import reverse


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ сервера')
    mailing = models.ForeignKey('mailings.Mailing', on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['-attempt_time']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['mailing']),
            models.Index(fields=['attempt_time']),
        ]

    def __str__(self):
        return f"Попытка #{self.id} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('attempts:detail', kwargs={'pk': self.pk})