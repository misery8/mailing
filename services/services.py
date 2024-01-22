import logging
import os

from django.db import transaction
from django.utils import timezone
import requests
from requests.exceptions import (
    Timeout,
    RequestException
)

from dto.models import (
    Client,
    ClientAttribute,
    MailingSettings,
    Notification,
    NotificationStatus,
    NotificationStatistics,
)
from config.celery import app


logger = logging.getLogger(__name__)

EXTERNAL_SERVICE_URL = 'https://probe.fbrq.cloud/v1/send/'
EXTERNAL_SERVICE_TOKEN = os.getenv('TOKEN')


@transaction.atomic
def create_client_attribute(client: Client) -> None:

    tags = list(client.tags.all())
    attribute_exists = ClientAttribute.objects.filter(
        operator_code=client.operator_code,
        tags=tags
    ).exists()

    if attribute_exists:
        return

    ClientAttribute.objects.create(
        operator_code=client.operator_code,
        tags=tags
    )


def get_clients_to_notify(mailing_settings: MailingSettings) -> list[int]:

    clients = ClientAttribute.objects.filter(
        mailing_settings=mailing_settings
    ).values_list('client', flat=True)

    return list(client.id for client in clients)


@app.task
@transaction.atomic
def send_notifications_for_clients(
        mailing_settings_id: int,
        client_ids: list[int]
) -> None:

    clients = Client.objects.filter(id__in=client_ids)
    mailing_settings = MailingSettings.objects.get(id=mailing_settings_id)
    for client in clients:
        instance = Notification.objects.create(
            client=client,
            mailing_settings=mailing_settings
        )
        send_notification(instance)
        create_notification_statistic(instance, client)


@app.task
def send_notification(notification: Notification) -> None:

    headers = {'Authorization': f'Bearer {EXTERNAL_SERVICE_TOKEN}'}

    payload = {
        "id": notification.id,
        "phone": notification.client.phone_number,
        "text": notification.mailing_settings.message_text,
    }

    try:
        response = requests.post(
            f'{EXTERNAL_SERVICE_URL}/{notification.id}',
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        notification.status = NotificationStatus.SENT
        logger.info(f'Notification {notification.id} sent successfully')
    except Timeout:
        notification.status = NotificationStatus.FAILED
        logger.error(f'Request to {EXTERNAL_SERVICE_TOKEN}/{notification.id} time out')
    except RequestException as e:
        notification.status = NotificationStatus.FAILED
        logger.error(f'Error sending notification {notification.id}: {e}')
    except Exception as e:
        notification.status = NotificationStatus.FAILED
        logger.exception(f'Unexpected error: {e}')

    notification.save()


def get_mailing() -> list[MailingSettings]:

    now = timezone.now()
    mailing_settings = MailingSettings.objects.filter(
        start_time__lte=now,
        end_time__gt=now
    )

    return list(mailing_settings)


def create_notification_statistic(
        notification: Notification,
        client: Client
) -> None:

    NotificationStatistics.objects.create(
        notification=notification,
        client=client,
        status=notification.status
    )
