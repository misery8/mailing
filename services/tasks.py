import os

import requests

from config.celery import app
from dto.models import StatusMailing
from .services import (
    get_messages
)

TOKEN = os.getenv('TOKEN')


@app.task
def send_client_notification():

    messages = get_messages()
    for message in messages:
        response = requests.post(
            f'https://probe.fbrq.cloud/v1/send/{message.id}',
            headers={'Authorization': f'Bearer {TOKEN}'},
            json={
                'id': message.id,
                'phone': message.client.phone_number,
                'text': message.mailing.message
            }
        )
        if response.status_code == 201:
            message.status = StatusMailing.sending
        else:
            message.status = StatusMailing.error
        message.save()
