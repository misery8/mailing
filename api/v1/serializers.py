from rest_framework import serializers

from dto.models import (
    Client,
    Mailing,
    Message
)


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('name', 'phone_number', 'tag', 'mobile_code')
        read_only_fields = ('id',)


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        fields = ('date_start', 'date_end', 'message', 'attribute_filter')
        read_only_fields = ('id',)


class MailingStatisticDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'client', 'mailing', 'status', 'created_at')


class MailingStatisticList(serializers.Serializer):

    mailing = serializers.CharField()
    status = serializers.CharField()
    count_of_messages = serializers.IntegerField()
