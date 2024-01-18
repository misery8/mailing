import datetime

from django.db.models import QuerySet

from dto.models import (
    Message,
    StatusMailing,
)


def get_messages() -> QuerySet[Message]:

    time_now = datetime.datetime.now()

    return Message.objects.filter(
        status__in=[StatusMailing.error, StatusMailing.new],
        mailing__date_start_gte=time_now,
        mailing__date_end_lte=time_now
    )
