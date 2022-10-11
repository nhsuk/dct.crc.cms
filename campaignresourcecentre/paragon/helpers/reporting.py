import json
import logging
import requests

logger = logging.getLogger(__name__)


def send_report(event_type, params={}):

<<<<<<< HEAD
    url = settings.REPORTING_ENDPOINT
    payload = json.dumps({"payload": params, "event": event_type, "group": "crc"})
=======
    # queue = "queue={}".format(settings.REPORTING_QUEUE)
    # message = ""
    # query_string = "queue={}&message={}".format(queue, message)
    # url = "{}?{}".format(settings.REPORTING_ENDPOINT, query_string)

    url = settings.REPORTING_ENDPOINT
    payload = json.dumps(
        {"queue": settings.REPORTING_QUEUE, "message": params, "event": event_type}
    )
>>>>>>> registration reporting test

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }

    if settings.REPORTING_ENABLED:
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.ok:
                logger.info(
<<<<<<< HEAD
                    "Successfully sent reporting data for user {} : {}".format(
                        event_type, response.content
                    )
                )
            else:
                logger.info(
                    "Error sending reporting data for user {} : {}".format(
                        event_type, response.content
                    )
=======
                    "Successfully sent {} report: {}".format(event_type, response)
                )
            else:
                logger.info(
                    "Error sending {} report: {}".format(event_type, response.content)
>>>>>>> registration reporting test
                )
        except Exception as err:
            logger.error("Exception raised : %s", err)
    else:
        logger.info("Reporting is not enabled")
