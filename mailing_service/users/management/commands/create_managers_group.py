from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clients.models import Client
from mailings.models import Mailing
from my_messages.models import Message


class Command(BaseCommand):
    help = 'Создает группу менеджеров с необходимыми правами доступа'

    def handle(self, *args, **options):
        # Создаем или получаем группу менеджеров
        managers_group, created = Group.objects.get_or_create(name='Менеджеры')

        if created:
            self.stdout.write('Группа "Менеджеры" создана')
        else:
            self.stdout.write('Группа "Менеджеры" уже существует')

        # Получаем разрешения для моделей
        client_content_type = ContentType.objects.get_for_model(Client)
        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        message_content_type = ContentType.objects.get_for_model(Message)

        # Добавляем разрешения для менеджеров
        permissions = Permission.objects.filter(
            content_type__in=[client_content_type, mailing_content_type, message_content_type],
            codename__in=[
                'can_view_all_clients',
                'can_block_client',
                'can_view_all_mailings',
                'can_disable_mailing',
                'can_block_mailing',
                'can_view_all_messages',
                'can_block_message',
            ]
        )

        managers_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f'Группе "Менеджеры" назначено {permissions.count()} разрешений'
            )
        )