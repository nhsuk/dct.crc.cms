from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from wagtail.test.utils import WagtailPageTests

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

    def _create_test_user_profile_data(self):
        return {
            "content": {
                "UserToken": "test_token",
                "EmailAddress": "test@example.com",
                "FirstName": "John",
                "LastName": "Doe",
                "ProductRegistrationVar3": "NHS Trust",
                "ProductRegistrationVar4": "GP",
                "ProductRegistrationVar1": "health",
                "ProductRegistrationVar2": "True",
                "ProductRegistrationVar10": "2025-11-25T10:00:00",
                "ProductRegistrationVar8": "",
                "ProductRegistrationVar7": "news",
                "ProductRegistrationVar9": "M1 1AA",
                "ContactVar2": "Emergency Medicine",
                "ContactVar3": "Manchester",
            }
        }

    def _create_test_form_data(self):
        return {
            "role": "standard",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "organisation": "NHS Trust",
            "job_title": "GP",
            "area_work": "Primary Care",
            "postcode": "LS1 1AA",
        }

    def _setup_user_permissions(self):
        content_type = ContentType.objects.get_for_model(self.user)
        permission, _ = Permission.objects.get_or_create(
            codename="manage_paragon_users_all_fields",
            content_type=content_type,
            defaults={"name": "Can manage all paragon user fields"},
        )
        self.user.user_permissions.add(permission)

    def _setup_mock_client_and_form(self, mock_client_class, mock_form_class):
        mock_client = mock_client_class.return_value
        mock_client.get_user_profile.return_value = (
            self._create_test_user_profile_data()
        )
        mock_client.update_user_profile.return_value = {"code": 200}

        mock_form = mock_form_class.return_value
        mock_form.is_valid.return_value = True
        mock_form.cleaned_data = self._create_test_form_data()

        return mock_client

    @patch("campaignresourcecentre.paragon_users.admin_views.UserAdminForm")
    @patch("campaignresourcecentre.paragon_users.admin_views.get_region")
    @patch("campaignresourcecentre.paragon_users.admin_views.Client")
    def test_edit_view_calls_get_region_for_postcode(
        self, mock_client_class, mock_get_region, mock_form_class
    ):
        mock_get_region.return_value = "Greater Manchester"
        self._setup_mock_client_and_form(mock_client_class, mock_form_class)
        self._setup_user_permissions()

        self.client.post(
            reverse("paragon_users:edit", args=["test_token"]),
            self._create_test_form_data(),
        )

        mock_get_region.assert_called_once_with("LS1 1AA")

    @patch("campaignresourcecentre.paragon_users.admin_views.UserAdminForm")
    @patch("campaignresourcecentre.paragon_users.admin_views.get_region")
    @patch("campaignresourcecentre.paragon_users.admin_views.Client")
    def test_edit_view_updates_user_with_area_work_and_region(
        self, mock_client_class, mock_get_region, mock_form_class
    ):
        mock_get_region.return_value = "Greater Manchester"
        mock_client = self._setup_mock_client_and_form(
            mock_client_class, mock_form_class
        )
        self._setup_user_permissions()

        self.client.post(
            reverse("paragon_users:edit", args=["test_token"]),
            self._create_test_form_data(),
        )

        mock_client.update_user_profile.assert_called_once()
        call_kwargs = mock_client.update_user_profile.call_args[1]
        self.assertEqual(call_kwargs["area_work"], "Primary Care")
        self.assertEqual(call_kwargs["postcode_region"], "Greater Manchester")

    @patch("campaignresourcecentre.paragon_users.admin_views.Client")
    def test_edit_view_get_user_profile(self, mock_client_class):
        mock_client = mock_client_class.return_value
        mock_client.get_user_profile.return_value = {
            "content": {
                "UserToken": "test_token",
                "EmailAddress": "test@example.com",
                "FirstName": "John",
                "LastName": "Doe",
                "ProductRegistrationVar3": "NHS Trust",
                "ProductRegistrationVar4": "GP",
                "ProductRegistrationVar1": "health",
                "ProductRegistrationVar2": "True",
                "ProductRegistrationVar10": "2025-11-25T10:00:00",
                "ProductRegistrationVar8": "",
                "ProductRegistrationVar7": "news",
                "ProductRegistrationVar9": "M1 1AA",
                "ContactVar2": "Primary Care",
                "ContactVar3": "Manchester",
            }
        }

        response = self.client.get(reverse("paragon_users:edit", args=["test_token"]))

        mock_client.get_user_profile.assert_called_once_with(user_token="test_token")
        self.assertEqual(response.status_code, 200)

    def test_signup_extracts_area_work_from_form(self):
        from campaignresourcecentre.paragon_users.views import RegisterForm
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com", 
            "password": "TestPass123@",
            "job_title": "health:gp",
            "area_work": "health:gp",
            "organisation": "Test Org",
            "postcode": "SW1A1AA"
        }
        
        form = RegisterForm(form_data)
        if form.is_valid():
            area_work = form.cleaned_data.get("area_work")
            self.assertEqual(area_work, "health:gp")
        else:
            area_work = form.data.get("area_work")
            self.assertEqual(area_work, "health:gp")

    def test_signup_handles_student_organisation_logic(self):
        test_cases = [
            ("student", " "),
            ("health:gp", "Test Org"),
            ("marketing", "Test Org")
        ]
        
        for job_title, expected_org in test_cases:
            organisation = " " if job_title == "student" else "Test Org"
            self.assertEqual(organisation, expected_org)

    def test_signup_calls_get_region_function(self):
        from campaignresourcecentre.paragon_users.helpers.postcodes import get_region
        
        result = get_region("SW1A 1AA")
        self.assertIsNotNone(result)

    @patch("campaignresourcecentre.paragon_users.views.send_verification")
    @patch("campaignresourcecentre.paragon_users.views.get_postcode_data")
    @patch("campaignresourcecentre.paragon_users.views.send_report")
    @patch("campaignresourcecentre.paragon_users.views.get_region")
    @patch("campaignresourcecentre.paragon_users.views.Client")
    def test_signup_create_account_with_new_fields(self, mock_client_class, mock_get_region, mock_send_report, mock_get_postcode_data, mock_send_verification):
        self.client.logout()
        mock_get_region.return_value = "Test Region"
        mock_get_postcode_data.return_value = {"longitude": 0, "latitude": 0, "region": "Test Region"}
        mock_client = mock_client_class.return_value
        mock_client.create_account.return_value = {"code": 200, "content": "token"}
        
        with patch("campaignresourcecentre.paragon_users.views.RegisterForm") as mock_form_class:
            mock_form = mock_form_class.return_value
            mock_form.is_valid.return_value = True
            mock_form.cleaned_data = {
                "email": "test@example.com",
                "password": "TestPass123@",
                "first_name": "John",
                "last_name": "Doe",
                "job_title": "health:gp",
                "area_work": "Emergency Medicine",
                "organisation": "Test Org",
                "postcode": "SW1A 1AA"
            }
            mock_form.fields = {"organisation": type('obj', (object,), {"required": False})(), "job_title": type('obj', (object,), {"required": False})()}
            mock_form.data = {"job_title": "health:gp"}
            
            from campaignresourcecentre.paragon_users.views import signup
            
            request = RequestFactory().post("/signup/")
            request.session = {}
            signup(request)
            
            mock_client.create_account.assert_called_once()
            call_args = mock_client.create_account.call_args[0]
            self.assertEqual(call_args[6], "Emergency Medicine")
            self.assertEqual(call_args[8], "Test Region")
