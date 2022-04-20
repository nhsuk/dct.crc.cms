from collections import defaultdict
import dataclasses
import logging
from typing import Dict, List, Protocol

from django.conf import settings
from django_gov_notify.message import NotifyEmailMessage

from .dataclasses import ContactUsData

logger = logging.getLogger(__name__)


def gov_notify_factory(use_fake=False):
    """Function to return a `GovNotifyNotifications` instance.

    Using this function rather than instantiating in code directly allows
    `FakeNotifications` to be used during development if `NOTIFY_DEBUG` is True
    in settings like `dev.py`."""

    if use_fake or getattr(settings, "NOTIFY_DEBUG", False):
         return FakeNotifications()
    return GovNotifyNotifications()


class AbstractNotifications(Protocol):
    """Interface to define the notification calls that can be made."""

    def review_page(
        self, recipients: List, page_title: str, page_edit_url: str
    ) -> None:
        """Notification for when a page is due for review."""

    def confirm_registration(
        self, email_address: str, first_name: str, verify_link: str
    ) -> None:
        """Notification to confirm to a user that their registration was
        successful."""

    def reset_password(
        self, email_address: str, first_name: str, reset_link: str
    ) -> None:
        """Notification to allow a user to reset their password."""

    def contact_submission(self) -> None:
        """Notification to send the Partnerships team data that has been
        submitted via the Contact Us form."""

    def contact_submission_user(self):
        """Notification to the user to confirm their contact us form has been
        submitted."""


class FakeNotifications:
    """Fake notification implementation for use in tests or debugging.

    Methods log to console and save to `self.sent`. Tests can use a
    `FakeNotifications` object like a `dict` for checking that it was called
    the correct arguments e.g:

        notifications = FakeNotifications()
        notifications.review_page(key=value)
        assert key in notifications
    """

    def __init__(self):
        self.sent = defaultdict(dict)  # type: Dict[str, Dict]

    def __contains__(self, key):
        return key in self.sent

    def __getitem__(self, key):
        return self.sent[key]

    def __call__(self):
        """Return self when called, useful for using as a mock object."""
        return self

    def review_page(
        self, recipients: List, page_title: str, page_edit_url: str
    ) -> None:
        self.sent[page_title] = {
            "recipients": recipients,
            "page_edit_url": page_edit_url,
        }
        logger.info(
            f"Emailing {recipients} about reviewing page {page_title}: {page_edit_url}"
        )

    def confirm_registration(
        self, email_address: str, first_name: str, verify_link: str
    ) -> None:
        self.sent[email_address] = {
            "first_name": first_name,
            "verify_link": verify_link,
        }
        logger.info(
            f"Emailing {first_name} ({email_address}) to confirm registration: {verify_link}"
        )

    def reset_password(
        self, email_address: str, first_name: str, reset_link: str
    ) -> None:
        self.sent[email_address] = {
            "first_name": first_name,
            "reset_link": reset_link,
        }
        logger.info(
            f"Emailing {first_name} ({email_address}) to reset password: {reset_link}"
        )

    def contact_submission(
        self, email_address: str, subject: str, submission_data: ContactUsData
    ) -> None:
        self.sent[email_address] = {
            "subject": subject,
            "submission_data": submission_data,
        }
        logger.info(
            f"Emailing team {email_address} about the {subject} form submission: {submission_data}"
        )

    def contact_submission_user(
        self, email_address: str, subject: str, submission_data: ContactUsData
    ) -> None:
        self.sent[email_address] = {
            "subject": subject,
            "submission_data": submission_data,
        }
        logger.info(
            f"Emailing user {email_address} about their {subject} form submission: {submission_data}"
        )


class GovNotifyNotifications:
    """Notification implementation for GOV.UK Notify."""

    # Template IDs from the GOV.UK Notify service.
    REVIEW_PAGE_TEMPLATE_ID = "b9f9c36d-dba5-4091-8345-e3c1a439374a"
    CONFIRM_REGISTRATION_TEMPLATE_ID = "84687efc-1829-45c8-afab-3cfdd220641e"
    RESET_PASSWORD_TEMPLATE_ID = "8d87349a-e520-48e5-afe8-1ada1df1f49e"
    CONTACT_SUBMISSION_TEMPLATE_ID = "eaee6094-f8f3-407e-aa92-94bd46bbc938"
    CONTACT_SUBMISSION_USER_TEMPLATE_ID = "e028940f-dec6-46bd-9de3-6ad916ae699c"

    def review_page(
        self, recipients: List, page_title: str, page_edit_url: str
    ) -> None:
        """Notify template:
        https://www.notifications.service.gov.uk/services/5516fd78-9e45-450a-8d50-87139dfc2d30/templates/b9f9c36d-dba5-4091-8345-e3c1a439374a
        """
        message = NotifyEmailMessage(
            to=recipients,
            template_id=self.REVIEW_PAGE_TEMPLATE_ID,
            personalisation={
                "page_title": page_title,
                "page_edit_url": page_edit_url,
            },
        )
        message.send()

    def confirm_registration(
        self, email_address: str, first_name: str, verify_link: str
    ) -> None:
        """Notify template:
        https://www.notifications.service.gov.uk/services/5516fd78-9e45-450a-8d50-87139dfc2d30/templates/84687efc-1829-45c8-afab-3cfdd220641e
        """
        message = NotifyEmailMessage(
            to=[email_address],
            template_id=self.CONFIRM_REGISTRATION_TEMPLATE_ID,
            personalisation={
                "first_name": first_name,
                "verify_link": verify_link,
            },
        )
        message.send()

    def reset_password(
        self, email_address: str, first_name: str, reset_link: str
    ) -> None:
        """Notify template:
        https://www.notifications.service.gov.uk/services/5516fd78-9e45-450a-8d50-87139dfc2d30/templates/8d87349a-e520-48e5-afe8-1ada1df1f49e
        """
        message = NotifyEmailMessage(
            to=[email_address],
            template_id=self.RESET_PASSWORD_TEMPLATE_ID,
            personalisation={
                "first_name": first_name,
                "password_reset_link": reset_link,
            },
        )
        message.send()

    def contact_submission(
        self, email_address: str, subject: str, submission_data: ContactUsData
    ) -> None:
        """Notify template:
        https://www.notifications.service.gov.uk/services/5516fd78-9e45-450a-8d50-87139dfc2d30/templates/eaee6094-f8f3-407e-aa92-94bd46bbc938
        """
        personalisation = dataclasses.asdict(submission_data)
        personalisation["subject"] = subject
        message = NotifyEmailMessage(
            to=[email_address],
            template_id=self.CONTACT_SUBMISSION_TEMPLATE_ID,
            personalisation=personalisation,
        )
        message.send()

    def contact_submission_user(
        self, email_address: str, subject: str, submission_data: ContactUsData
    ) -> None:
        """Notify template:
        https://www.notifications.service.gov.uk/services/5516fd78-9e45-450a-8d50-87139dfc2d30/templates/e028940f-dec6-46bd-9de3-6ad916ae699c
        """
        personalisation = dataclasses.asdict(submission_data)
        personalisation["subject"] = subject
        message = NotifyEmailMessage(
            to=[email_address],
            template_id=self.CONTACT_SUBMISSION_USER_TEMPLATE_ID,
            personalisation=personalisation,
        )
        message.send()
