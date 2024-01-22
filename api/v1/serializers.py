from rest_framework import serializers

from dto.models import (
    Client,
    MailingSettings,
    Notification,
    NotificationStatistics,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)

    class Meta:
        model = Client
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingSettings
        fields = '__all__'


class NotificationStatisticsSerializer(serializers.ModelSerializer):



    class Meta:
        model = NotificationStatistics
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
