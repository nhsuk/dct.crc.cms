import datetime

from freezegun import freeze_time

from django.test import TestCase

from ..factories import PageLifecyclePageFactory


@freeze_time("2021-04-26")
class PageLifecycleFormTestCase(TestCase):
    def test_next_review_date_changed_when_last_reviewed_changed(self):
        """If the last reviewed date is changed then the next review date
        should also be updated."""
        page = PageLifecyclePageFactory()
        self.assertEqual(page.last_reviewed, datetime.date.fromisoformat("2021-04-26"))
        self.assertEqual(page.next_review, datetime.date.fromisoformat("2022-04-26"))

        form_class = page.get_edit_handler().get_form_class()
        form = form_class(
            {
                "last_reviewed": datetime.date.fromisoformat("2021-05-01"),
                "title": page.title,
                "slug": page.slug,
            },
            instance=page,
        )
        self.assertTrue(form.is_valid())
        form.save()

        page.refresh_from_db()
        self.assertEqual(page.last_reviewed, datetime.date.fromisoformat("2021-05-01"))
        self.assertEqual(page.next_review, datetime.date.fromisoformat("2022-05-01"))

    def test_next_review_not_changed_if_last_reviewed_not_changed(self):
        """If the last reviewed date is not changed then the next review date
        should not be updated."""
        page = PageLifecyclePageFactory()
        self.assertEqual(page.last_reviewed, datetime.date.fromisoformat("2021-04-26"))
        self.assertEqual(page.next_review, datetime.date.fromisoformat("2022-04-26"))

        form_class = page.get_edit_handler().get_form_class()
        form = form_class(
            {
                "last_reviewed": datetime.date.fromisoformat("2021-04-26"),
                "title": page.title,
                "slug": page.slug,
            },
            instance=page,
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(page.last_reviewed, datetime.date.fromisoformat("2021-04-26"))
        self.assertEqual(page.next_review, datetime.date.fromisoformat("2022-04-26"))
