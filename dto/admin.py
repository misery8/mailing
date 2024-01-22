from django.contrib import admin

from .models import (
    Client,
    MailingSettings,
    Notification,
    Tag,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number')


@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'client')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
