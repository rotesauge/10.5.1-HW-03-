from django.apps import AppConfig


class NewsboardappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsboardapp'

    def ready(self):
        import  newsboardapp.signals