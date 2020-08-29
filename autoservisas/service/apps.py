from django.apps import AppConfig


class ServiceConfig(AppConfig):
    name = 'service'

    def ready(self):
        from .signals import create_profile, save_profile