from rest_framework import serializers

from dto.models import (
    Client,
    Mailing,
    Message, Tag
)


class ClientSerializer(serializers.ModelSerializer):

    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Client
        fields = ('id', 'name', 'phone_number', 'tag', 'mobile_code', 'timezone')
        read_only_fields = ('id',)


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        fields = ('id', 'date_start', 'date_end', 'message', 'attribute_filter')
        read_only_fields = ('id',)


class MailingStatisticDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'client', 'mailing', 'status', 'created_at')


class MailingStatisticList(serializers.Serializer):

    mailing = serializers.CharField()
    status = serializers.CharField()
    count_of_messages = serializers.IntegerField()
