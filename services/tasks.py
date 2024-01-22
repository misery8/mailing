from celery import shared_task

from .services import (
    get_mailing,
    send_notifications_for_clients,
    get_clients_to_notify,
)


@shared_task
def process_mailing():

    mailing_settings = get_mailing()
    for setting in mailing_settings:
        clients_to_notify = get_clients_to_notify(setting)
        send_notifications_for_clients(
            mailing_settings_id=setting.id,
            client_ids=clients_to_notify
        )


@shared_task
def process_notifications(mailing_ids: list[int]) -> None:
    # TODO: Проверка рассылок на временной интервал
    pass

