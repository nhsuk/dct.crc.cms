import json
import logging
import requests

logger = logging.getLogger(__name__)


def send_report(event_type, params={}):

    # message = ""
    # query_string = "message={}".format(message)
    # url = "{}?{}".format(settings.REPORTING_ENDPOINT, query_string)

    url = settings.REPORTING_ENDPOINT
    payload = json.dumps({"message": params, "event": event_type})

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
                logger.info(
                    "Error sending reporting data for user {} : {}".format(
                        event_type, response.content
                    )
                )
        except Exception as err:
            logger.error("Exception raised : %s", err)
    else:
        logger.info("Reporting is not enabled")
