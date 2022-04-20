import datetime

from freezegun import freeze_time

from django.test import TestCase

from ..factories import PageLifecyclePageFactory


@freeze_time("2021-04-26")
class PageLifecycleMixinTestCase(TestCase):
    def test_last_reviewed_date_default_is_set(self):
        page = PageLifecyclePageFactory()
        self.assertEqual(page.last_reviewed, datetime.date.fromisoformat("2021-04-26"))

    def test_next_review_date_default_is_set(self):
        page = PageLifecyclePageFactory()
        self.assertEqual(page.next_review, datetime.date.fromisoformat("2022-04-26"))
