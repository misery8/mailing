import zoneinfo

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Название тега')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ClientAttribute(models.Model):

    operator_code = models.CharField(max_length=6)
    tags = models.ManyToManyField(Tag, related_name='tags')

    class Meta:
        verbose_name = 'Атрибут клиента'
        verbose_name_plural = 'Атрибуты клиентов'


class Client(models.Model):

    operator_code_validator = RegexValidator(
        regex=r'^\+\d{1,5}$',  # Паттерн для кода мобильного оператора: + и от 1 до 5 цифр
        message='Код мобильного оператора должен начинаться с символа "+"'
    )

    phone_number_validator = RegexValidator(
        regex=r'^7\d{10}$',  # Паттерн для номера телефона: 7 и 10 цифр
        message='Номер телефона должен быть в формате 7XXXXXXXXXX'
    )

    name = models.CharField(max_length=255, verbose_name=_('Наименование'))
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[phone_number_validator],
        verbose_name='Номер телефона'
    )
    operator_code = models.CharField(
        max_length=6,
        validators=[operator_code_validator],
        verbose_name='Код мобильного оператора'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    timezone = models.CharField(
        choices=tuple(zip(zoneinfo.available_timezones(), zoneinfo.available_timezones())),
        default='Europe/Moscow',
        verbose_name=_('Часовой пояс')
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):

    start_time = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    message_text = models.TextField(verbose_name='Текст сообщения')
    client_filter = models.ManyToManyField(
        ClientAttribute,
        related_name='mailing_settings',
        verbose_name='Фильтр клиентов'
    )

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылок'


class NotificationStatus(models.TextChoices):
    SENT = 'Sent', 'Отправлено'
    FAILED = 'Failed', 'Ошибка'


class Notification(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания'
    )
    status = models.CharField(
        max_length=10,
        choices=NotificationStatus.choices,
        default=NotificationStatus.SENT,
        verbose_name='Статус'
    )
    mailing_settings = models.ForeignKey(
        MailingSettings,
        on_delete=models.CASCADE,
        verbose_name='Настройка рассылки'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class NotificationStatistics(models.Model):

    notification = models.ForeignKey(
        'Notification',
        on_delete=models.CASCADE,
        verbose_name=_('Уведомление')
    )
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name=_('Клиент')
    )
    status = models.CharField(
        max_length=10,
        choices=NotificationStatus.choices,
        verbose_name=_('Статус')
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата и время отправки')
    )

    class Meta:
        verbose_name = _('Статистика уведомления')
        verbose_name_plural = _('Статистика уведомлений')
