from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.urls import reverse
from wagtail.test.utils import WagtailPageTests
from django.contrib.auth import get_user_model

from campaignresourcecentre.paragon_users.admin_views import search_users
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import (
    ParagonClientError,
    ParagonClientTimeout,
)
from campaignresourcecentre.users.models import User
from django.contrib.auth import get_user_model


class ParagonUsersTestCase(WagtailPageTests):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@example.com",
            password="password",
            is_active=True,
            is_superuser=True,
        )

        self.client.login(username="test", password="password")

    def test_index_page_loads(self):
        response = self.client.get(reverse("paragon_users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "paragon_users/index.html")

    def test_search_users_success(self):
        with patch.object(Client, "search_users") as mock_search_users:
            mock_search_users.return_value = self.getDummyResponse()

            response = self.client.get(
                reverse("paragon_users:search_users"),
                {"q": "test", "limit": "20", "p": "1"},
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "paragon_users/results.html")

    def test_search_users_timeout(self):
        with patch.object(Client, "search_users") as mock_search_users:
            mock_search_users.side_effect = ParagonClientTimeout

            response = self.client.get(
                reverse("paragon_users:search_users"),
                {"q": "test", "limit": "20", "p": "1"},
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "paragon_users/results.html")

            self.assertEqual(
                response.context_data["error_message"],
                "The request to the service took too long to respond.",
            )

    def test_search_users_not_found(self):
        with patch.object(Client, "search_users") as mock_search_users:
            mock_search_users.side_effect = ParagonClientError(
                "No records match the criteria"
            )

            response = self.client.get(
                reverse("paragon_users:search_users"),
                {"q": "test", "limit": "20", "p": "1"},
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "paragon_users/results.html")
            self.assertEqual(
                response.context_data["error_message"],
                "Error: No users found for search: test",
            )

    def getDummyResponse(self):
        return {
            "content": [
                {
                    "UserToken": "token token",
                    "ProductToken": "the product",
                    "Title": "mr",
                    "FirstName": "r",
                    "LastName": "c",
                    "EmailAddress": "testemail@email.com",
                    "ContactVar1": "1",
                    "ContactVar2": "1",
                    "ContactVar3": "1",
                    "ContactVar4": "1",
                    "ContactVar5": "1",
                    "ProductRegistrationVar1": "standard",  # or "uber"
                    "ProductRegistrationVar2": "True",
                    "ProductRegistrationVar3": "A mockery",
                    "ProductRegistrationVar4": "other",
                    "ProductRegistrationVar5": "1",
                    "ProductRegistrationVar6": "true",
                    "ProductRegistrationVar7": "1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "ProductRegistrationVar8": "2024-03-11T11:21:32",
                    "ProductRegistrationVar9": "WC1 2AA",
                    "ProductRegistrationVar10": "2024-03-11T11:21:32",
                }
            ]
        }


def _mock_user(verified=False):
    return {
        "content": {
            "EmailAddress": "test@example.com",
            "ProductRegistrationVar2": str(verified),
            "ProductRegistrationVar4": "other",
            "ProductRegistrationVar9": "WC1 2AA",
        }
    }


class VerificationViewTestCase(TestCase):
    """After verifying their email, a user's session should be flushed so they
    must log in again — this ensures their session has fresh verified data."""

    VIEWS = "campaignresourcecentre.paragon_users.views"

    def setUp(self):
        self.mock_unsign = patch(
            f"{self.VIEWS}.unsign", return_value="user-token"
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
