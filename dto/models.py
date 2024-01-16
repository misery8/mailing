import pytz

from django.db import models

TIMEZONE = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class StatusMailing(models.TextChoices):
    sending = 'sending'
    received = 'received'
    error = 'error'


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Client(models.Model):

    name = models.CharField(verbose_name='Имя клиента')
    phone_number = models.PositiveIntegerField(
        verbose_name='Номер телефона',
        unique=True
    )
    mobile_code = models.CharField(
        verbose_name='Код мобильного оператора',
        max_length=2
    )
    tag = models.ManyToManyField('Tag', verbose_name='Тег')
    timezone = models.CharField(
        verbose_name='Часовой пояс',
        max_length=36,
        choices=TIMEZONE,
        default='Europe/Moscow'
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return set(self.name)


class Mailing(models.Model):

    date_start = models.DateTimeField(verbose_name='Дата начала')
    date_end = models.DateTimeField(verbose_name='Дата окончания')
    message = models.TextField(verbose_name='Текст уведомления')
    attribute_filter = models.ManyToManyField(
        'ClientProperty',
        verbose_name='Фильтр свойств клиентов'
    )

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'


class Message(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status = models.CharField(verbose_name='Статус', choices=StatusMailing.choices)
    client = models.OneToOneField(
        'Client',
        verbose_name='Клиент',
        on_delete=models.CASCADE
    )
    mailing = models.OneToOneField(
        'Mailing',
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
        related_name='mailing'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.status}-{self.client} - {self.created_at}'


class ClientProperty(models.Model):

    mobile_code = models.CharField(max_length=2, verbose_name='Код мобильного оператора')
    tag = models.ForeignKey(
        'Tag',
        verbose_name='Тег',
        on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = 'Фильтр свойств клиента'
        verbose_name_plural = 'Фильтры свойств клиентов'

    def __str__(self):
        return f'{self.mobile_code}/{str(self.tag)}'
