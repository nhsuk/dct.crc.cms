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
                    "ContactVar2": "Emergency Medicine",
                    "ContactVar3": "London",
                    "ContactVar4": "1",
                    "ContactVar5": "1",
                    "ProductRegistrationVar1": "standard",
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

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.get_region")
    @patch("campaignresourcecentre.paragon.client.Client")
    def test_signup_with_area_work_and_location_data(
        self, mock_client_class, mock_get_region
    ):
        from campaignresourcecentre.paragon_users.helpers.postcodes import get_region

        mock_get_region.return_value = "London"
        mock_client = mock_client_class.return_value

        area_work = "Primary Care"
        postcode = "SW1A 1AA"
        postcode_region = get_region(postcode)

        self.assertEqual(postcode_region, "London")
        mock_get_region.assert_called_once_with("SW1A 1AA")

        mock_client.create_account(
            "test@example.com",
            "TestPass123@",
            "John",
            "Doe",
            "NHS Trust",
            "health:gp",
            area_work,
            postcode,
            postcode_region,
            "2025-11-25 10:00:00",
        )

        call_args = mock_client.create_account.call_args[0]
        self.assertEqual(call_args[6], "Primary Care")
        self.assertEqual(call_args[8], "London")

    @patch("campaignresourcecentre.paragon.client.Client")
    def test_user_profile_update_with_work_area_and_location(self, mock_client_class):
        from campaignresourcecentre.paragon.client import Client

        mock_client = mock_client_class.return_value
        client = Client()

        client.update_user_profile(
            user_token="test_token",
            area_work="General Practice",
            postcode_region="Yorkshire",
            postcode="LS1 1AA",
        )

        mock_client.update_user_profile.assert_called_once_with(
            user_token="test_token",
            area_work="General Practice",
            postcode_region="Yorkshire",
            postcode="LS1 1AA",
        )

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.get_region")
    def test_postcode_to_region_mapping_during_registration(self, mock_get_region):
        from campaignresourcecentre.paragon_users.helpers.postcodes import get_region

        mock_get_region.return_value = "Greater Manchester"

        postcodes_and_expected_regions = [
            ("M1 1AA", "Greater Manchester"),
            ("SW1A 1AA", "Greater Manchester"),
            ("B1 1AA", "Greater Manchester"),
        ]

        for postcode, expected_region in postcodes_and_expected_regions:
            with self.subTest(postcode=postcode):
                result = get_region(postcode)
                self.assertEqual(result, expected_region)

        self.assertEqual(mock_get_region.call_count, 3)
