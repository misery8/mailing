from django.contrib import admin

from .models import (
    Client,
    Mailing,
    Message
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number')
