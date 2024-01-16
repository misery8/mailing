from django.db.models import Count
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from dto.models import (
    Client,
    Mailing,
    Message,
)
from .serializers import (
    ClientSerializer,
    MailingSerializer,
    MailingStatisticDetailSerializer,

)


class ClientCreateAPIView(CreateAPIView):

    """ Добавления нового клиента """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientAPIView(RetrieveUpdateDestroyAPIView):

    """
    Обновление данных атрибутов клиента.
    Удаления клиента из справочника
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingCreateAPIView(CreateAPIView):
    """ Добавление новой рассылки """

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingStatisticListAPIView(ListAPIView):

    """
    Получение общей статистики по созданным рассылкам
     и количеству отправленных сообщений по ним
    """

    def get_queryset(self):
        return (
            Message.objects.all()
            .values('status', 'mailing_id')
            .annotate(
                count_of_message=Count('id')
            )
        )
        # Общее количество сообщений отправленных с группировкой по статусу
        # SELECT COUNT(msg.id) as count_of_message,
        # mailing.id
        # msg.status
        # FROM mailing inner join message as msg on mailing.id = msg.mailing_id


class MailingStatisticDetailAPIView(RetrieveAPIView):

    """
    Получение детальной статистики, отправленных сообщений по конкретной рассылке
    """
    queryset = Message.objects.all()
    serializer_class = MailingStatisticDetailSerializer


class MailingAPIView(RetrieveUpdateDestroyAPIView):

    """ Обновление данных рассылки """

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
