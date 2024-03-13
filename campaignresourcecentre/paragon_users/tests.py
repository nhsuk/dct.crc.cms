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

        self.standardUser = get_user_model().objects.create_user(
            username="standard",
            email="standard@example.com",
            password="password",
            is_active=True,
            is_superuser=False,
        )

        self.client.login(username="test", password="password")

    def test_index_page_loads(self):
        response = self.client.get(reverse("paragon_users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "paragon_users/index.html")

    def test_user_is_redirected_without_permissions(self):
        self.client.login(username=self.standardUser.username, password="password")
        response = self.client.get(reverse("paragon_users:index"))
        self.assertEqual(response.status_code, 302)

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

            print(response)

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
