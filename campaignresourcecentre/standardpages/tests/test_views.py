import logging
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from wagtail.test.utils import WagtailPageTests

from ..views import UpdateIndexThread

logger = logging.getLogger(__name__)


class UpdateIndexTestCases(WagtailPageTests):
    url = "/crc-admin/update_index/"

    def setUp(self):
        self.superuser = get_user_model().objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            is_active=True,
            is_superuser=True,
        )

        self.regular_user = get_user_model().objects.create_user(
            username="regular",
            email="regular@example.com",
            password="testpass123",
            is_active=True,
            is_superuser=False,
        )

    @patch("campaignresourcecentre.standardpages.views.call_command")
    def test_update_index_runs_on_separate_thread(self, mock_call_command):
        thread = UpdateIndexThread()
        thread.run()
        mock_call_command.assert_called_once_with("update_index")

    def test_user_not_logged_in_and_no_auth_headers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_update_index_no_pubtoken(self):
        auth_headers = {}
        response = self.client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, 401)

    @override_settings(PUBTOKEN="correct")
    def test_has_authorization_header_with_wrong_pubtoken(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer incorrect",
        }
        response = self.client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, 401)

    @patch("campaignresourcecentre.standardpages.views.call_command")
    @override_settings(PUBTOKEN="correct")
    def test_has_authorization_header_with_correct_pubtoken(self, mock_call_command):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer correct",
        }
        response = self.client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, 200)
        mock_call_command.assert_called_once_with("update_index")

    def test_no_authorization_header_logged_in_without_superuser(self):
        self.client.login(username="regular", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    @patch("campaignresourcecentre.standardpages.views.call_command")
    def test_no_authorization_header_logged_in_with_superuser(self, mock_call_command):
        self.client.login(username="admin", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Index update started")
        mock_call_command.assert_called_once_with("update_index")
