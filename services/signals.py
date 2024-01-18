from datetime import timedelta

from celery.schedules import crontab
from django.db.models.signals import (
    post_save,
    pre_delete,
    m2m_changed
)
from django.dispatch import receiver
from django.db.utils import IntegrityError

from dto.models import (
    Mailing,
    Client,
    ClientProperty,
    Message
)
from config import celery_app


@receiver(m2m_changed, sender=Mailing.attribute_filter.through)
def create_mailing_list(sender, instance: Mailing, action, **kwargs):

    if action == 'post_add':
        clients_attributes_data = instance.attribute_filter.all()
        clients_attributes = {}
        for attr in clients_attributes_data:
            if clients_attributes.get(attr.mobile_code):
                clients_attributes[attr.mobile_code].add(attr.tag.id)
            else:
                clients_attributes[attr.mobile_code] = {attr.tag.id}

        filterset = {
            'mobile_code__in': list(clients_attributes.keys()),
            'tag__in': list(*clients_attributes.values())
        }
        clients = Client.objects.filter(**filterset)
        for client in clients:
            try:
                Message.objects.create(
                    client=client,
                    mailing=instance
                )
            except IntegrityError:
                pass


@receiver(m2m_changed, sender=Client.tag.through)
def save_client_property(sender, instance: Client, action, **kwargs):

    """ Сохраняем свойства клиента, для дальнейшей фильтрации по ним """

    if action == 'post_add':
        for tag in instance.tag.all():
            if not ClientProperty.objects.filter(tag=tag, mobile_code=instance.mobile_code).exists():
                ClientProperty.objects.create(
                    tag=tag,
                    mobile_code=instance.mobile_code
                )
