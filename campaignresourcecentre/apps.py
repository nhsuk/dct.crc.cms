import logging
import os
from sys import argv

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class CRCV3Config(AppConfig):
    name = "campaignresourcecentre"
    verbose_name = "Campaign Resource Centre V3"

    def ready(self):
        # Avoid showing output once for main thread and again for reloader if in use
        if os.environ.get("RUN_MAIN", "").lower() != "true":
            logger.info("Starting CRC-V3")
            logger.info(
                "Debug: %s Paragon mock: %s" % (settings.DEBUG, settings.PARAGON_MOCK)
            )
            if os.environ.get("WEB_CONCURRENCY"):
                logger.info(
                    "Concurrency: %s Options: '%s'"
                    % (
                        os.environ.get("WEB_CONCURRENCY"),
                        os.environ.get("GUNICORN_CMD_ARGS"),
                    )
                )
            logger.info("Cache: %s" % settings.CACHES)
            logger.info("File storage: %s", settings.DEFAULT_FILE_STORAGE)
            logger.info("Search storage: %s", settings.SEARCH_STORAGE_CLASS)
            logger.info("Updating Azure search: %s", settings.AZURE_SEARCH_UPDATE)
            # If using runserver we must force CONN_MAX_AGE to zero or
            # database connection limit will be exceeded under heavy loads
            if len(argv) >= 2 and argv[1] == "runserver":
                default_database = settings.DATABASES.get("default")
                if default_database and default_database.get("CONN_MAX_AGE") != 0:
                    logger.info("Forcing connection max age to zero for runserver")
                    default_database["CONN_MAX_AGE"] = 0
