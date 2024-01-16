from django.contrib import admin

from .models import (
    Client,
    Mailing,
    Message,
    Tag,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_start', 'date_end')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'client')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
