import datetime
import logging

from freezegun import freeze_time

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase, override_settings

from campaignresourcecentre.notifications.adapters import FakeNotifications

from ..factories import PageLifecyclePageFactory
from ..utils import (
    calculate_next_review_date,
    get_next_review_duration,
    get_pages_for_review_notifications,
    send_page_review_notifications,
)

logger = logging.getLogger(__name__)
User = get_user_model()


@freeze_time("2021-04-26")
@override_settings(PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION=12)
class CalculateNextReviewDateTest(TestCase):
    def test_returns_date_from_today_if_none_passed(self):
        """If a date isn't passed then it should return the date
        `PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION` months in the future from
        today."""
        self.assertEqual(
            calculate_next_review_date(), datetime.date.fromisoformat("2022-04-26")
        )

    def test_returns_correct_future_date_when_date_passed(self):
        """If a date is passed then it should return the date
        `PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION` months in the future from
        the date."""
        self.assertEqual(
            calculate_next_review_date(date=datetime.date.fromisoformat("2021-01-31")),
            datetime.date.fromisoformat("2022-01-31"),
        )

    def test_returns_correct_future_date_when_leap_year(self):
        """If a leap year date is passed then it should return the appropriate
        date `PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION` months in the future."""
        self.assertEqual(
            calculate_next_review_date(date=datetime.date.fromisoformat("2020-02-29")),
            datetime.date.fromisoformat("2021-02-28"),
        )


class GetNextReviewDurationTestCase(TestCase):
    @override_settings(PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION=7)
    def test_fetches_from_settings(self):
        self.assertEqual(get_next_review_duration(), 7)

    @override_settings(PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION="test")
    def test_returns_default_if_not_int(self):
        self.assertEqual(get_next_review_duration(), 12)

    @override_settings()
    def test_returns_default_if_not_set(self):
        del settings.PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION
        self.assertEqual(get_next_review_duration(), 12)


@freeze_time("2021-04-26")
class GetPagesForReviewNotificationsTestCase(TestCase):
    def test_fetches_pages_with_review_date_today(self):
        today = datetime.date.fromisoformat("2021-04-26")
        # patch the PageLifecyclePage to be createable
        PageLifecyclePageFactory._meta.model.is_creatable = True
        page1 = PageLifecyclePageFactory(next_review=today)
        page2 = PageLifecyclePageFactory(next_review=today)
        page3 = PageLifecyclePageFactory(
            next_review=datetime.date.fromisoformat("2021-01-31")
        )
        pages = get_pages_for_review_notifications()
        self.assertIn(page1, pages)
        self.assertIn(page2, pages)
        self.assertNotIn(page3, pages)

    def test_does_not_fetch_pages_lifecycle_test_page(self):
        today = datetime.date.fromisoformat("2021-04-26")
        PageLifecyclePageFactory(next_review=today)
        pages = get_pages_for_review_notifications()
        self.assertEqual([], pages)


class SendPageReviewNotificationsTestCase(TestCase):
    """Test the page review notification function."""

    def test_sends_to_notification_email(self):
        email = "bob@test.com"
        notifications = FakeNotifications()
        page = PageLifecyclePageFactory()
        send_page_review_notifications([page], notifications, email)
        self.assertIn(email, notifications[page.title]["recipients"])

    def test_sends_to_page_owner(self):
        email = "user@test.com"
        notifications = FakeNotifications()
        page = PageLifecyclePageFactory(owner=User.objects.create(email=email))
        send_page_review_notifications([page], notifications)
        self.assertIn(email, notifications[page.title]["recipients"])

    def test_sends_to_pages_with_owners(self):
        notifications = FakeNotifications()
        page1 = PageLifecyclePageFactory(
            owner=User.objects.create(email="user1@test.com", username="user1")
        )
        page2 = PageLifecyclePageFactory(
            owner=User.objects.create(email="user2@test.com", username="user2")
        )
        page3 = PageLifecyclePageFactory()
        send_page_review_notifications([page1, page2, page3], notifications)
        self.assertIn(page1.title, notifications)
        self.assertIn(page2.title, notifications)
        self.assertNotIn(page3.title, notifications)

    def test_passes_page_parameters(self):
        """Tests that it passes the page title and edit URL to the send
        function. This may change when email (Notify?) is implemented."""
        email = "user@test.com"
        notifications = FakeNotifications()
        page = PageLifecyclePageFactory()
        send_page_review_notifications([page], notifications, email)
        self.assertEqual(
            notifications[page.title],
            {
                "recipients": [email],
                "page_edit_url": f"/crc-admin/pages/{page.id}/edit/",
            },
        )
