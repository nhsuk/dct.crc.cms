from logging import getLogger

from campaignresourcecentre.paragon_users.helpers.token_signing import sign
from campaignresourcecentre.paragon_users.models import VerificationEmail
from urllib.parse import quote
from campaignresourcecentre.notifications.adapters import gov_notify_factory

logger = getLogger(__name__)


def send_verification(token, url, email, first_name):
    # sign token
    token = sign(token)
    url = url + "?q=" + quote(token)
    # send email
    try:
        email_client = gov_notify_factory()
        email_client.confirm_registration(email, first_name, url)
    except Exception as e1:
        logger.error("Error sending verification email: %s", e1)
        try:
            logger.error(
                "Recording email failure (field lengths %d, %d, %d, %d)",
                len(token),
                len(email),
                len(url),
                len(first_name),
            )
            verification_email = VerificationEmail(
                user_token=token, email=email, url=url, first_name=first_name
            )
            verification_email.save()
        except Exception as e2:
            # Sometimes even recording the send failure fails,
            # log it but the main problem to raise is the the send failure itself
            logger.error("Failed to record email send failure: %s", e2)
        raise
