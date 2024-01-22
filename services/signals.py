from typing import Any

from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from django.utils import timezone

from dto.models import (
    Client,
    MailingSettings,
)
from .services import (
    create_client_attribute,
    get_clients_to_notify,
    send_notifications_for_clients,
)


@receiver(post_save, sender=Client)
def handle_client_post_save(
        sender: type(Client),
        instance: Client,
        created: bool,
        **kwargs: Any
) -> None:

    create_client_attribute(instance)


@receiver(post_save, sender=MailingSettings)
def handle_mailing_settings_post_save(
        sender: type(MailingSettings), instance, created, **kwargs):

    if created:
        current_time = timezone.now()

        if instance.start_time <= current_time <= instance.end_time:
            clients_to_notify = get_clients_to_notify(instance)
            # Запуск отправки уведомлений для выбранных клиентов
            send_notifications_for_clients.delay(instance.id, clients_to_notify)
