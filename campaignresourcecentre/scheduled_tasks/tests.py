from django.test import TestCase, override_settings
import logging


logger = logging.getLogger(__name__)


class ScheduledTasksTestCase(TestCase):

    url = "/crc-admin/pub"

    def test_publish_pages_no_pubtoken(self):
        auth_headers = {}
        response = self.client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, 403)

    @override_settings(PUBTOKEN="correct")
    def test_publish_pages_wrong_pubtoken(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer incorrect",
        }
        response = self.client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, 403)

    @override_settings(PUBTOKEN="correct")
    def test_publish_pages_correct_pubtoken(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer correct",
        }
        response = self.client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, 202)
