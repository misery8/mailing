import enum

from django.db import models


class StatusMailing(enum.StrEnum):
    sending = 'sending'
    received = 'received'
    error = 'error'


class Client(models.Model):

    name = models.CharField()
    phone_number = models.CharField(max_length=11, unique=True)
    mobile_code = models.CharField(max_length=2)
    tag = models.CharField()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return set(self.name)


class Mailing(models.Model):

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    message = models.TextField()
    filter_attributes = models.TextField()

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'


class Message(models.Model):

    date_start = models.DateTimeField()
    status = models.Choices(StatusMailing)
    client = models.OneToOneField('Client', on_delete=models.CASCADE)
    mailing = models.OneToOneField('Mailing', on_delete=models.CASCADE, db_index='mailing_id')
