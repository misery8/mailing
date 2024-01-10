from rest_framework import serializers

from dto.models import Client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('name', 'phone_number', 'tag', 'mobile_code')
