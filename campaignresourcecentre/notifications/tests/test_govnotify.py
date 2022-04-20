import dataclasses
import unittest
import uuid

from django.conf import settings
from django.test import TestCase, override_settings

from faker import Faker

from notifications_python_client.notifications import NotificationsAPIClient

from ..adapters import FakeNotifications, GovNotifyNotifications, gov_notify_factory
from ..dataclasses import ContactUsData

GOVUK_NOTIFY_TEST_API_KEY = getattr(settings, "GOVUK_NOTIFY_TEST_API_KEY", None)


class GovNotifyFactoryTestCase(TestCase):
    """Test that the gov_notify_factory function returns the correct object."""

    @override_settings(NOTIFY_DEBUG=True)
    def test_returns_fake_for_setting(self):
        self.assertTrue(isinstance(gov_notify_factory(), FakeNotifications))

    @override_settings(NOTIFY_DEBUG=False)
    def test_returns_fake_for_parameter(self):
        self.assertTrue(
            isinstance(gov_notify_factory(use_fake=True), FakeNotifications)
        )

    @override_settings(NOTIFY_DEBUG=False)
    def test_returns_real(self):
        self.assertTrue(isinstance(gov_notify_factory(), GovNotifyNotifications))

    @override_settings()
    def test_returns_real_if_no_setting(self):
        del settings.NOTIFY_DEBUG
        self.assertTrue(isinstance(gov_notify_factory(), GovNotifyNotifications))


@unittest.skipUnless(GOVUK_NOTIFY_TEST_API_KEY, "GOVUK_NOTIFY_TEST_API_KEY is not set")
@override_settings(GOVUK_NOTIFY_API_KEY=GOVUK_NOTIFY_TEST_API_KEY)
class GovNotifyNotificationsTestCase(TestCase):
    """Integration tests for the GOV.UK Notify adapter.

    Individual methods are tested by sending a notification request to a sandbox
    "Test – pretends to send messages" Notify API key, and then checking that
    a corresponding message with the correct data exists on the Notify service.

    Add the sandbox API key to the Django setting: `GOVUK_NOTIFY_TEST_API_KEY`.

    These tests interact with the GOV.UK Notify service so it might be worth
    running them periodically rather than on every local dev or CI test run.
    """

    def setUp(self):
        self.notifications = GovNotifyNotifications()
        self.notifications_client = NotificationsAPIClient(GOVUK_NOTIFY_TEST_API_KEY)

    def get_unique_email(self):
        uid = str(uuid.uuid4())
        return f"{uid}@test.com"

    def get_notification(self, email_address):
        response = self.notifications_client.get_all_notifications(
            template_type="email"
        )
        try:
            return next(
                x
                for x in response["notifications"]
                if x["email_address"] == email_address
            )
        except StopIteration:
            self.fail(f"Notification to {email_address} not found.")

    def get_contact_submission_data(self, email_address=None):
        fake = Faker()
        return ContactUsData(
            email_address or fake.free_email(),
            fake.first_name(),
            fake.last_name(),
            fake.job(),
            fake.company(),
            fake.company_suffix(),
            fake.word(),
            fake.word(),
            fake.word(),
            fake.word(),
            fake.text(),
        )

    def test_review_page(self):
        email_address1 = self.get_unique_email()
        email_address2 = self.get_unique_email()
        page_title = "Test Page"
        edit_url = "/crc-admin/edit/123/"

        self.notifications.review_page(
            [email_address1, email_address2], page_title, edit_url
        )

        notification1 = self.get_notification(email_address1)
        self.assertEqual(
            GovNotifyNotifications.REVIEW_PAGE_TEMPLATE_ID,
            notification1["template"]["id"],
        )
        self.assertIn(page_title, notification1["body"])
        self.assertIn(edit_url, notification1["body"])
        notification2 = self.get_notification(email_address2)
        self.assertEqual(
            GovNotifyNotifications.REVIEW_PAGE_TEMPLATE_ID,
            notification2["template"]["id"],
        )
        self.assertIn(page_title, notification2["body"])
        self.assertIn(edit_url, notification2["body"])

    def test_confirm_registration(self):
        email_address = self.get_unique_email()
        first_name = "Rich Test"
        verify_link = "www.test.com/verify/"

        self.notifications.confirm_registration(email_address, first_name, verify_link)

        notification = self.get_notification(email_address)
        self.assertEqual(
            GovNotifyNotifications.CONFIRM_REGISTRATION_TEMPLATE_ID,
            notification["template"]["id"],
        )
        self.assertIn(first_name, notification["body"])
        self.assertIn(verify_link, notification["body"])

    def test_reset_password(self):
        email_address = self.get_unique_email()
        first_name = "Rich Test"
        reset_link = "www.test.com/reset/"

        self.notifications.reset_password(email_address, first_name, reset_link)

        notification = self.get_notification(email_address)
        self.assertEqual(
            GovNotifyNotifications.RESET_PASSWORD_TEMPLATE_ID,
            notification["template"]["id"],
        )
        self.assertIn(first_name, notification["body"])
        self.assertIn(reset_link, notification["body"])

    def test_contact_submission(self):
        email_address = self.get_unique_email()
        subject = "Contact Us"
        submission_data = self.get_contact_submission_data()

        self.notifications.contact_submission(email_address, subject, submission_data)

        notification = self.get_notification(email_address)
        self.assertEqual(
            GovNotifyNotifications.CONTACT_SUBMISSION_TEMPLATE_ID,
            notification["template"]["id"],
        )
        self.assertIn(subject, notification["subject"])
        for value in dataclasses.asdict(submission_data).values():
            with self.subTest(value=value):
                self.assertIn(value, notification["body"])

    def test_contact_submission_user(self):
        email_address = self.get_unique_email()
        subject = "Contact Us"
        submission_data = self.get_contact_submission_data()

        self.notifications.contact_submission_user(
            email_address, subject, submission_data
        )

        notification = self.get_notification(email_address)
        self.assertEqual(
            GovNotifyNotifications.CONTACT_SUBMISSION_USER_TEMPLATE_ID,
            notification["template"]["id"],
        )
        self.assertIn(subject, notification["subject"])
        for value in dataclasses.asdict(submission_data).values():
            with self.subTest(value=value):
                self.assertIn(value, notification["body"])
