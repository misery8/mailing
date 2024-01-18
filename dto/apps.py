from django.apps import AppConfig


class DTOConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dto'
    verbose_name = 'Каталоги'

    def ready(self):
        import services.signals
