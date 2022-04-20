from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = "campaignresourcecentre.orders"

    def ready(self):
        from . import signal_handlers  # noqa
