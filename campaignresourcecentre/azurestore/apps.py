from django.apps import AppConfig


class AzurestoreConfig(AppConfig):
    name = "campaignresourcecentre.azurestore"

    def ready(self):
        from . import signal_handlers  # noqa
