from django.core.management.base import BaseCommand
from django.utils import timezone
from mailings.models import Mailing
from mailings.services import send_mailing_service


class Command(BaseCommand):
    help = 'Отправляет рассылку по ID или все запланированные рассылки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mailing-id',
            type=int,
            help='ID конкретной рассылки для отправки',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Отправить все запланированные рассылки',
        )

    def handle(self, *args, **options):
        mailing_id = options.get('mailing_id')
        send_all = options.get('all')

        if mailing_id:
            # Отправка конкретной рассылки
            try:
                mailing = Mailing.objects.get(id=mailing_id)
                self.stdout.write(f'Отправка рассылки #{mailing.id}...')
                success, failure = send_mailing_service(mailing)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Рассылка #{mailing.id} отправлена. '
                        f'Успешно: {success}, Ошибок: {failure}'
                    )
                )
            except Mailing.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена')
                )

        elif send_all:
            # Отправка всех запланированных рассылок
            now = timezone.now()
            mailings = Mailing.objects.filter(
                status__in=[Mailing.STATUS_CREATED, Mailing.STATUS_STARTED],
                start_time__lte=now,
                end_time__gte=now
            )

            self.stdout.write(f'Найдено {mailings.count()} рассылок для отправки')

            for mailing in mailings:
                self.stdout.write(f'Отправка рассылки #{mailing.id}...')
                success, failure = send_mailing_service(mailing)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Рассылка #{mailing.id} отправлена. '
                        f'Успешно: {success}, Ошибок: {failure}'
                    )
                )

        else:
            self.stdout.write(
                self.style.WARNING(
                    'Укажите --mailing-id ID_рассылки или --all для отправки всех рассылок'
                )
            )

