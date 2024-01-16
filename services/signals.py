from django.db.models.signals import (
    post_save,
    pre_delete,
)
from django.dispatch import receiver

from dto.models import (
    Mailing,
    Client,
    ClientProperty,
)
from tasks import celery_app


@receiver(post_save, sender=Mailing)
def mailing_create_task(sender, instance, created, **kwargs):

    pass


@receiver(post_save, sender=Client)
def add_client_property(sender, instance, created, **kwargs):

    """ Сохраняем свойства клиента, для дальнейшей фильтрации по ним """

    if created:

        ClientProperty.objects.create(
            tag=instance.tag,
            mobile_code=instance.mobile_code
        )
