from unittest.mock import patch

from django.test import TestCase

from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError
from campaignresourcecentre.paragon_users.helpers.newsletter import serialise


def _mock_user_profile(subscriptions=None):
    return {
        "content": {
            "ProductRegistrationVar7": subscriptions or serialise({}),
            "ProductRegistrationVar2": "True",
        }
    }


class NewsletterPreferencesViewTestCase(TestCase):
    """Tests for the logged-in newsletter preferences view."""

    URL = "/account/newsletters/"

    def setUp(self):
        session = self.client.session
        session["ParagonUser"] = "logged-in-token"
        session["Verified"] = "True"
        session.save()

        patch.object(
            Client,
            "get_user_profile",
            return_value=_mock_user_profile(),
        ).start()
        self.mock_update = patch.object(
            Client, "update_user_profile", return_value=True
        ).start()
        self.addCleanup(patch.stopall)

    def test_get_renders_preference_form(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/newsletter_preferences.html")
        self.assertIn("form", response.context)

    def test_get_populates_form_from_api(self):
        response = self.client.get(self.URL)
        form = response.context["form"]
        self.assertIsNotNone(form.initial)

    def test_post_calls_api_with_user_token(self):
        self.client.post(self.URL, {"AllAges": "on"})
        self.mock_update.assert_called_once()
        call_kwargs = self.mock_update.call_args[1]
        self.assertEqual(call_kwargs["user_token"], "logged-in-token")

    def test_post_saves_preferences_and_shows_confirmation(self):
        response = self.client.post(self.URL, {"AllAges": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_newsletters.html")

    def test_confirmation_back_link_points_to_account(self):
        response = self.client.post(self.URL, {"AllAges": "on"})
        self.assertEqual(response.context["back_link"], "/account/newsletters/")

    def test_post_unsubscribe_all_shows_unsubscribed_page(self):
        response = self.client.post(self.URL, {"unsubscribe_all": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_unsubscribed.html")

    def test_unsubscribe_all_back_link_points_to_account(self):
        response = self.client.post(self.URL, {"unsubscribe_all": ""})
        self.assertEqual(response.context["back_link"], "/account/newsletters/")

    def test_unsubscribe_all_sends_all_false_to_api(self):
        self.client.post(self.URL, {"unsubscribe_all": ""})
        call_kwargs = self.mock_update.call_args[1]
        # All preferences should be "0" (False)
        self.assertTrue(all(c == "0" for c in call_kwargs["subscriptions"]))

    def test_post_api_error_redisplays_form_with_errors(self):
        patch.object(
            Client,
            "update_user_profile",
            side_effect=ParagonClientError("Something went wrong"),
        ).start()

        response = self.client.post(self.URL, {"AllAges": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/newsletter_preferences.html")
        self.assertTrue(response.context["form"].errors)
