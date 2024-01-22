from django.db.models import Count
from django.utils import timezone
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    extend_schema_view,
)
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from dto.models import (
    Client,
    MailingSettings,
    NotificationStatistics,
    Notification,
    NotificationStatus,
    Tag,
)
from .serializers import (
    ClientSerializer,
    MailingSerializer,
    NotificationStatisticsSerializer,
    NotificationSerializer,
    TagSerializer
)
from services.tasks import process_notifications


@extend_schema_view(tags=['api/v1'])
class ClientViewSet(viewsets.ModelViewSet):

    """ Управление CRUD операциями над моделью Client """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @extend_schema(
        methods=['get'],
        operation_id='get_client_list',
        description='Получение списка клиентов.',
        responses={200: ClientSerializer(many=True)},
        parameters=[OpenApiParameter(name='phone_number', description='Фильтр по номеру телефона')]
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Получение списка клиентов.

        Параметры:
        - phone_number: Фильтр по номеру телефона

        Пример использования:
        GET /api/v1/clients
        """
        queryset = self.filter_queryset(self.get_queryset())
        phone_number = request.query_params.get('phone_number', None)
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        methods=['get'],
        operation_id='get_client_details',
        description='Получение деталей конкретного клиента.',
        responses={200: ClientSerializer},
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Получение деталей конкретного клиента.

        Пример использования:
        GET /api/v1/clients/{pk}/
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        methods=['post'],
        operation_id='create_client',
        description='Создание нового клиента.',
        responses={201: ClientSerializer}
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание нового клиента

        Пример использования:
        POST /api/v1/clients/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tags_data = request.data.pop('tags', [])
        tags_serializer = TagSerializer(data=tags_data, many=True)
        tags_serializer.is_valid(raise_exception=True)

        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_data]

        Client.objects.create(**request.data, tags=tags)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @extend_schema(
        methods=['patch'],
        operation_id='partial_update_client',
        description='Частичное обновление данных клиента.',
        responses={200: ClientSerializer}
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """
        Частичное обновление данных клиента.

        Пример использования:
        PATCH /api/v1/clients/{pk}/
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        methods=['delete'],
        operation_id='delete_client',
        description='Удаление клиента.',
        responses={204: 'No Content'}
    )
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление клиента

        Пример использования:
        DELETE /api/v1/clients/{pk}/
        """
        return super().destroy(request, *args, **kwargs)


# @extend_schema_view(tags=['api/v1'])
class MailingViewSet(viewsets.ModelViewSet):
    """ Добавление новой рассылки """

    queryset = MailingSettings.objects.all()
    serializer_class = MailingSerializer

    # @extend_schema(
    #     methods=['post'],
    #     operation_id='create_mailing_settings',
    #     description='Создать рассылку.',
    #     responses={201: MailingSerializer}
    # )
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Создать рассылку

        Пример использования:
        POST /api/v1/mailings/
        """
        return super().create(request, *args, **kwargs)

    # @extend_schema(
    #     methods=['get'],
    #     operation_id='get_mailings',
    #     description='Получение список рассылок.',
    #     responses={200: MailingSerializer(many=True)}
    # )
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Получение список рассылок

        Пример использования:
        GET /api/v1/mailings/
        """
        return super().list(request, *args, **kwargs)

    # @extend_schema(
    #     methods=['get'],
    #     operation_id='get_mailing',
    #     description='Получение деталей конкретной рассылки.',
    #     responses={200: MailingSerializer}
    # )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Получение деталей конкретной рассылки

        Пример использования:
        GET /api/v1/mailings/{pk}/
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        methods=['patch'],
        operation_id='partial_update_mailing',
        description='Частичное обновление данных рассылки.',
        responses={200: MailingSerializer}
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """
        Частичное обновление данных рассылки

        Пример использования:
        PATCH /api/v1/mailings/{pk}/
        """
        return super().partial_update(request, *args, **kwargs)

    # @extend_schema(
    #     methods=['delete'],
    #     operation_id='delete_mailing',
    #     description='Удаление рассылки.',
    #     responses={204: 'No Content'}
    # )
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление рассылки

        Пример использования:
        DELETE /api/v1/mailings/{pk}/
        """
        return super().destroy(request, *args, **kwargs)


# @extend_schema_view(tags=['api/v1'])
class NotificationStatisticsViewSet(
    generics.ListAPIView,
    generics.RetrieveAPIView
):

    queryset = NotificationStatistics.objects.all()
    serializer_class = NotificationStatisticsSerializer

    @extend_schema(
        methods=['get'],
        operation_id='get_general_statistics',
        description='''Получение общей статистики по созданным рассылкам')
            и количеству отправленных уведомлений по ним с группировкой по статусам.''',
        responses={200: NotificationStatisticsSerializer(many=True)}
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        general_statistics = NotificationStatistics.objects.values('status').annotate(count=Count('id'))

        serializer = self.get_serializer(general_statistics, many=True)
        return Response(serializer.data)

    @extend_schema(
        methods=['get'],
        operation_id='get_detailed_statistics',
        description='Получение детальной статистики отправленных уведомлений по конкретной рассылке.',
        responses={200: NotificationStatisticsSerializer(many=True)}
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:

        mailing_id = self.kwargs['mailing_id']
        detailed_statistics = (
            NotificationStatistics.objects.filter(
                notification__mailing_settings_id=mailing_id
            ).values('status', 'notification__mailing_settings__id')
            .annotate(count_of_send_notification=Count('id'))
        )
        serializer = self.get_serializer(detailed_statistics, many=True)
        return Response(serializer.data)


# @extend_schema_view(tags=['api/v1'])
class NotificationCreateAPIView(generics.CreateAPIView):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    # @extend_schema(
    #     methods=['post'],
    #     operation_id='process_active_mailing_notification',
    #     description='Обработка и рассылка активных уведомлений.',
    #     responses={201: dict[str: str]}
    # )
    def post(self, request: Request, *args, **kwargs) -> Response:

        time_now = timezone.now()
        active_mailings = Notification.objects.filter(
            status=NotificationStatus.FAILED,
            mailing_settings__start_time__gte=time_now,
            mailing_settings__end_time__lte=time_now
        ).values_list('mailing_id', flat=True)
        if len(active_mailings) == 0:
            return Response({'status': 'No active mailings'})

        process_notifications.delay(active_mailings)

        return Response({'status': 'Processing started'})
