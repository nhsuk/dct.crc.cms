"""
WSGI config for campaignresourcecentre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import logging
import os

from azure.monitor.opentelemetry import configure_azure_monitor

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "campaignresourcecentre.settings.production"
)

if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING") is not None:
    configure_azure_monitor()

    # This is a workaround for https://github.com/Azure/azure-sdk-for-python/issues/33623 to reduce verbose logging from the sdk
    logging.getLogger("azure.monitor.opentelemetry.exporter.export._base").setLevel(
        logging.WARNING
    )
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
        logging.WARNING
    )

application = get_wsgi_application()
