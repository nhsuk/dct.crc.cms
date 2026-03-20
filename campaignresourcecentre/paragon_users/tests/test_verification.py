from unittest.mock import patch
from django.test import TestCase
from campaignresourcecentre.paragon.client import Client


class VerificationViewTestCase(TestCase):
    """After verifying their email, a user's session should be flushed so they
    must log in again — this ensures their session has fresh verified data."""

    VIEWS = "campaignresourcecentre.paragon_users.views"

    def setUp(self):
        self.mock_unsign = patch(
            f"{self.VIEWS}.unsign_user_token", return_value="user-token"
        ).start()
        patch.object(Client, "get_user_profile", return_value=_mock_user()).start()
        patch.object(Client, "update_user_profile", return_value=True).start()
        patch(f"{self.VIEWS}.get_region", return_value="region.london").start()
        self.addCleanup(patch.stopall)

    def _set_session(self, **kwargs):
        session = self.client.session
        session.update(kwargs)
        session.save()

    def test_session_is_flushed_after_verification(self):
        self._set_session(ParagonUser="user-token", Verified="False")

        response = self.client.get("/verification/", {"q": "token"})

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("ParagonUser", self.client.session)
        self.assertNotIn("Verified", self.client.session)

    def test_anonymous_user_can_verify(self):
        response = self.client.get("/verification/", {"q": "token"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/confirmation_user_verification.html")

    def test_already_verified_user_is_redirected_home(self):
        patch.object(
            Client, "get_user_profile", return_value=_mock_user(verified=True)
        ).start()
        self._set_session(ParagonUser="user-token", Verified="True")

        response = self.client.get("/verification/", {"q": "token"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertEqual(self.client.session["ParagonUser"], "user-token")

    def test_missing_token_redirects_home(self):
        response = self.client.get("/verification/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_invalid_token_returns_400(self):
        self.mock_unsign.side_effect = Exception("bad token")

        response = self.client.get("/verification/", {"q": "bad token"})
        self.assertEqual(response.status_code, 400)

    def test_paragon_update_failure_returns_500(self):
        patch.object(Client, "update_user_profile", return_value=False).start()

        response = self.client.get("/verification/", {"q": "token"})
        self.assertEqual(response.status_code, 500)
