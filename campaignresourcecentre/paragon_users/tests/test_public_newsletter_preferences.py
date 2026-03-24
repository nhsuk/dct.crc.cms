from unittest.mock import patch

from django.test import TestCase

from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import (
    ParagonClientError,
    ParagonClientTimeout,
)
from campaignresourcecentre.paragon_users.helpers.newsletter import serialise


def _mock_user_profile(subscriptions=None):
    return {
        "content": {
            "ProductRegistrationVar7": subscriptions or serialise({}),
        }
    }


class PublicNewsletterPreferencesViewTestCase(TestCase):
    """Tests for the public newsletter preferences accessed via email link."""

    URL = "/newsletter-preferences/"

    def setUp(self):
        patch.object(
            Client,
            "get_user_profile",
            return_value=_mock_user_profile(),
        ).start()
        self.mock_update = patch.object(
            Client, "update_user_profile", return_value=True
        ).start()
        self.addCleanup(patch.stopall)

    def _post_with_preference(self, **extra):
        return self.client.post(
            f"{self.URL}?userToken=valid-token",
            {"AllAges": "on", **extra},
        )

    def test_missing_token_returns_404(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "users/public_preferences_not_found.html")

    def test_invalid_token_returns_404(self):
        patch.object(
            Client, "get_user_profile", side_effect=ParagonClientError("invalid")
        ).start()

        response = self.client.get(self.URL, {"userToken": "bad-token"})
        self.assertEqual(response.status_code, 404)

    def test_get_renders_preference_form(self):
        response = self.client.get(self.URL, {"userToken": "valid-token"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/public_newsletter_preferences.html")
        self.assertIn("form", response.context)

    def test_get_populates_form_from_api(self):
        response = self.client.get(self.URL, {"userToken": "valid-token"})
        form = response.context["form"]
        self.assertIsNotNone(form.initial)

    def test_post_calls_api_with_user_token(self):
        self._post_with_preference()
        self.mock_update.assert_called_once()
        call_kwargs = self.mock_update.call_args[1]
        self.assertEqual(call_kwargs["user_token"], "valid-token")

    def test_post_saves_preferences_and_shows_confirmation(self):
        response = self._post_with_preference()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_newsletters.html")

    def test_confirmation_back_link_includes_user_token(self):
        response = self._post_with_preference()
        self.assertEqual(
            response.context["back_link"],
            "/newsletter-preferences/?userToken=valid-token",
        )

    def test_post_unsubscribe_all_shows_unsubscribed_page(self):
        response = self.client.post(
            f"{self.URL}?userToken=valid-token",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_unsubscribed.html")

    def test_post_api_error_redisplays_form_with_errors(self):
        patch.object(
            Client,
            "update_user_profile",
            side_effect=ParagonClientError("Something went wrong"),
        ).start()

        response = self._post_with_preference()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/public_newsletter_preferences.html")
        self.assertTrue(response.context["form"].errors)
