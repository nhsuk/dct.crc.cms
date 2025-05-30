import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_report(event_type, params):
    jsondata = json.loads(params)
    url = settings.REPORTING_ENDPOINT
    payload = json.dumps(
        {"message": {"payload": jsondata, "event": event_type, "group": "crc"}}
    )

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }

    if settings.REPORTING_ENABLED:
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.ok:
                logger.info(
                    "Successfully sent reporting data for user {} : {}".format(
                        event_type, response.content
                    )
                )
            else:
                logger.error(
                    "Error sending reporting data for user {} : Code {} - {}".format(
                        event_type, response.status_code, response.content
                    )
                )
        except Exception as err:
            logger.error("Exception raised : %s", err)
    else:
        logger.info("Reporting is not enabled")
