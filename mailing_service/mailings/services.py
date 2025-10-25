from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from attempts.models import Attempt
from .models import Mailing


def send_mailing_service(mailing):
    # Обновляем статус рассылки
    mailing.update_status()

    # Если рассылка не активна, не отправляем
    if mailing.status != Mailing.STATUS_STARTED:
        return 0, 0

    # Если это первая отправка, сохраняем время
    if not mailing.first_sent:
        mailing.first_sent = timezone.now()
        mailing.save(update_fields=['first_sent'])

    success_count = 0
    failure_count = 0

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = Attempt.STATUS_SUCCESS
            response = 'Сообщение успешно отправлено'
            success_count += 1
        except Exception as e:
            status = Attempt.STATUS_FAILURE
            response = str(e)
            failure_count += 1

        Attempt.objects.create(
            mailing=mailing,
            client=client,
            status=status,
            server_response=response
        )

    # Проверяем статус после отправки
    mailing.update_status()

    return success_count, failure_count