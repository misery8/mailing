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
    MailingStatisticList,
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
    serializer_class = MailingStatisticList

    def get_queryset(self):
        return (
            Message.objects.all()
            .values('status', 'mailing_id')
            .annotate(
                count_of_message=Count('id')
            )
        )


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
