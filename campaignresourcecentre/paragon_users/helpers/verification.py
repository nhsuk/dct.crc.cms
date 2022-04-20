from campaignresourcecentre.paragon_users.helpers.token_signing import sign
from campaignresourcecentre.paragon_users.models import VerificationEmail
from urllib.parse import quote
from campaignresourcecentre.notifications.adapters import gov_notify_factory


def send_verification(token, url, email, first_name):
    # sign token
    token = sign(token)
    url = (url + "?q=" + quote(token))
    # send email
    try:
        emailClient = gov_notify_factory()
        emailClient.confirm_registration(email, first_name, url)
    except: # noqa
        vEmail = VerificationEmail(
            user_token=token,
            email=email,
            url=url,
            first_name=first_name)
        vEmail.save()
