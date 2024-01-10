from django.db.models.signals import (
    post_save,
    pre_delete,
)
from django.dispatch import receiver

from dto.models import Mailing


@receiver(post_save, sender=Mailing)
def create_task(sender, instance, created, **kwargs):
    pass
