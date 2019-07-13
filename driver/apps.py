from django.apps import AppConfig


class DriverConfig(AppConfig):
    name = 'driver'

    def ready(self):
        from .signals import announce_user