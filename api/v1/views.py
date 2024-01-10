from rest_framework.generics import (
    ListCreateAPIView,
    UpdateAPIView,
)

from dto.models import Client
from .serializers import ClientSerializer


class ClientsListCreateAPIView(ListCreateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientUpdateAPIView(UpdateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
