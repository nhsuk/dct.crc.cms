import datetime
import json
import responses

from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from .client import Client
from .data_classes import Registration, User, UpdatePassword, Address, CreateOrder

# NB plain from .exceptions imports app.campaignresourcecentre...
# which doesn't match the raised exception in assertRaises tests below
from campaignresourcecentre.paragon.exceptions import PasswordError


class TestClient(TestCase):
    def setUp(self):
        self.client = Client()

    @responses.activate
    def test_login(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/Login"),
            json="Token",
            status=200,
        )

        resp = self.client.login("testd@g.com", "Password")

        self.assertEqual({"code": 200, "content": "Token", "status": "ok"}, resp)

    @responses.activate
    def test_create_account(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/Signup"),
            json="Token",
            status=200,
        )

        email = "test2@test.com"
        password = "Test123@"
        first_name = "First Name"
        last_name = "Last Name"
        organisation = "NHS"
        job_title = "title"
        postcode = "S221LZ"
        postcode_region = "South Yorkshire"
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        resp = self.client.create_account(
            email,
            password,
            first_name,
            last_name,
            organisation,
            job_title,
            postcode,
            postcode_region,
            created_at,
        )

        self.assertEqual({"code": 200, "content": "Token", "status": "ok"}, resp)

    @responses.activate
    def test_create_account_includes_job_title_with_role_and_postcode_region(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/Signup"),
            json="Token",
            status=200,
        )

        email = "test@example.com"
        password = "Test123@"
        first_name = "John"
        last_name = "Doe"
        organisation = "Test Org"
        job_title_with_role = "health:gp"
        postcode = "SW1A 1AA"
        postcode_region = "London"
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")

        self.client.create_account(
            email,
            password,
            first_name,
            last_name,
            organisation,
            job_title_with_role,
            postcode,
            postcode_region,
            created_at,
        )

        self.assertEqual(len(responses.calls), 1)
        request_data = json.loads(responses.calls[0].request.body)

        self.assertEqual(request_data["ContactVar3"], postcode_region)
        self.assertEqual(request_data["EmailAddress"], email)
        self.assertEqual(request_data["ProductRegistrationVar3"], organisation)
        self.assertEqual(request_data["ProductRegistrationVar4"], job_title_with_role)
        self.assertEqual(request_data["ProductRegistrationVar9"], postcode)

    @responses.activate
    def test_search_users(self):
        api_url = "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/Search")
        responses.add(
            responses.POST, api_url, json=[{"email": "test@gmail.com"}], status=200
        )

        resp = self.client.search_users("test")

        self.assertEqual(
            {"code": 200, "content": [{"email": "test@gmail.com"}], "status": "ok"},
            resp,
        )

        responses.assert_call_count(count=1, url=api_url)
        request_json = json.loads(responses.calls[0].request.body)
        self.assertEqual(request_json["EmailAddress"], "test")
        self.assertEqual(request_json["SortColumn"], 0)
        self.assertEqual(request_json["Top"], 20)
        self.assertEqual(request_json["Offset"], 0)

    @responses.activate
    def test_search_users_specify_limit(self):
        api_url = "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/Search")
        responses.add(
            responses.POST, api_url, json=[{"email": "test@gmail.com"}], status=200
        )

        resp = self.client.search_users("test", limit=10)

        self.assertEqual(
            {"code": 200, "content": [{"email": "test@gmail.com"}], "status": "ok"},
            resp,
        )

        responses.assert_call_count(count=1, url=api_url)
        request_json = json.loads(responses.calls[0].request.body)
        self.assertEqual(request_json["Top"], 10)

    @responses.activate
    def test_search_users_specify_offset(self):
        api_url = "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/Search")
        responses.add(
            responses.POST, api_url, json=[{"email": "test@gmail.com"}], status=200
        )

        resp = self.client.search_users("test", offset=100)

        self.assertEqual(
            {"code": 200, "content": [{"email": "test@gmail.com"}], "status": "ok"},
            resp,
        )

        responses.assert_call_count(count=1, url=api_url)
        request_json = json.loads(responses.calls[0].request.body)
        self.assertEqual(request_json["Offset"], 100)

    @responses.activate
    def test_get_user_profile(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/RetrieveProfile"),
            json=[{"email": "test@gmail.com"}],
            status=200,
        )

        resp = self.client.get_user_profile("token")

        self.assertEqual(
            {"code": 200, "content": [{"email": "test@gmail.com"}], "status": "ok"},
            resp,
        )

    @responses.activate
    def test_update_user_profile(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/UpdateProfile"),
            json=[{"email": "test@gmail.com"}],
            status=200,
        )

        resp = self.client.update_user_profile(
            "token", "role", True, str(datetime.datetime.now()), "news"
        )

        self.assertEqual(
            {"code": 200, "content": [{"email": "test@gmail.com"}], "status": "ok"},
            resp,
        )

    @responses.activate
    def test_update_user_profile_with_job_role_and_postcode_region(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/UpdateProfile"),
            json={"success": True},
            status=200,
        )

        user_token = "test_token"
        job_title_with_role = "health:gp"
        postcode_region = "West Midlands"

        resp = self.client.update_user_profile(
            user_token,
            email="updated@example.com",
            first_name="Updated",
            last_name="User",
            job_title=job_title_with_role,
            postcode_region=postcode_region,
            postcode="B1 1AA",
        )

        self.assertEqual(len(responses.calls), 1)
        request_data = json.loads(responses.calls[0].request.body)
        self.assertEqual(request_data["ProductRegistrationVar4"], job_title_with_role)
        self.assertEqual(request_data["ContactVar3"], postcode_region)
        self.assertEqual(
            {"code": 200, "content": {"success": True}, "status": "ok"}, resp
        )

    @responses.activate
    def test_update_password(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/UpdatePassword"),
            json=[{"email": "test@gmail.com"}],
            status=200,
        )

        resp = self.client.update_password("token", "Test@123")

        self.assertEqual(
            {"code": 200, "content": [{"email": "test@gmail.com"}], "status": "ok"},
            resp,
        )

    @responses.activate
    def test_order_history(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/GetOrderHistory"),
            json=[{"order_number": "1"}],
            status=200,
        )

        start_date = end_date = str(datetime.datetime.now())
        resp = self.client.order_history("token", start_date, end_date, 1, 10)

        self.assertEqual(
            {"code": 200, "content": [{"order_number": "1"}], "status": "ok"}, resp
        )

    @responses.activate
    def test_set_user_address(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/SetDeliveryAddress"),
            json="True",
            status=200,
        )

        address_lines = {
            "address_1": "address line 1",
            "address_2": "address line 2",
            "address_3": "address line 3",
            "address_4": "address line 4",
            "address_5": "address line 5",
        }
        resp = self.client.set_user_address("token", address_lines)

        self.assertEqual({"code": 200, "content": "True", "status": "ok"}, resp)

    @responses.activate
    def test_create_order(self):
        responses.add(
            responses.POST,
            "{0}{1}".format(settings.PARAGON_API_ENDPOINT, "/CreateCheckout"),
            json="True",
            status=200,
        )

        order_items = [
            {
                "item_code": "ITEM1",
                "quantity": "2",
                "item_url": "https://test.com/item/1",
                "campaign": "test campaign",
                "image_url": "https://blobstorage.com/image1",
                "title": "Title",
            }
        ]
        resp = self.client.create_order("token", "1", order_items)

        self.assertEqual({"code": 200, "content": "True", "status": "ok"}, resp)


class TestRegistrationDataClass(TestCase):
    def test_valid_params(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "Test@123",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        expected_params = {
            "EmailAddress": "test@gmail.com",
            "Password": "Test@123",
            "FirstName": "First Name",
            "LastName": "Last Name",
            "ContactVar3": "South Yorkshire",
            "ProductRegistrationVar2": "False",
            "ProductRegistrationVar3": "NHS",
            "ProductRegistrationVar4": "health:gp",
            "ProductRegistrationVar6": "true",
            "ProductRegistrationVar7": "000000000000000000000000000000",
            "ProductRegistrationVar9": "SE1 9LT",
            "ProductRegistrationVar10": created_at,
        }
        self.assertEqual(expected_params, registration.params())

    def test_valid_optional_params(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "Test@123",
            "First Name",
            "Last Name",
            "NHS",
            "marketing",
            "SE1 9LT",
            None,
            created_at,
        )
        expected_params = {
            "EmailAddress": "test@gmail.com",
            "Password": "Test@123",
            "FirstName": "First Name",
            "LastName": "Last Name",
            "ContactVar3": None,
            "ProductRegistrationVar2": "False",
            "ProductRegistrationVar3": "NHS",
            "ProductRegistrationVar4": "marketing",
            "ProductRegistrationVar6": "true",
            "ProductRegistrationVar7": "000000000000000000000000000000",
            "ProductRegistrationVar9": "SE1 9LT",
            "ProductRegistrationVar10": created_at,
        }
        self.assertEqual(expected_params, registration.params())

    def assert_exception(self, error, message):
        self.assertEqual(str(error.exception), message)

    def test_raise_invalid_password(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "test@123",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(PasswordError) as error:
            registration.params()
        self.assert_exception(
            error,
            "Password must be at least 9 characters long, and contain at least 1 number, 1 capital letter, 1 lowercase letter and 1 symbol",
        )

    def test_raise_email_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "",
            "test123",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "email is empty!")

    def test_raise_password_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "password is empty!")

    def test_raise_first_name_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "test123",
            "",
            "Last Name",
            "NHS",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "first_name is empty!")

    def test_raise_last_name_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "test123",
            "First Name",
            "",
            "NHS",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "last_name is empty!")

    def test_raise_org_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "test123",
            "First Name",
            "Last Name",
            "",
            "health:gp",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "organisation is empty!")

    def test_raise_role_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "test123",
            "First Name",
            "Last Name",
            "NHS",
            "",
            "SE1 9LT",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "job_title is empty!")

    def test_raise_postcode_exception(self):
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        registration = Registration(
            "test@gmail.com",
            "test123",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",
            "",
            "South Yorkshire",
            created_at,
        )
        with self.assertRaises(ValueError) as error:
            registration.params()
        self.assert_exception(error, "postcode is empty!")


class TestUserDataClass(TestCase):
    def test_valid_params(self):
        verified_at = datetime.datetime.now()
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        update_user_profile = User(
            "token",
            "test@gmail.com",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",
            "role",
            True,
            created_at,
            verified_at,
            "news",
            "AB25 1CD",
            "postcode_region",
        )
        expected_params = {
            "UserToken": "token",
            "EmailAddress": "test@gmail.com",
            "FirstName": "First Name",
            "LastName": "Last Name",
            "ContactVar3": "postcode_region",
            "ProductRegistrationVar1": "role",
            "ProductRegistrationVar2": True,
            "ProductRegistrationVar3": "NHS",
            "ProductRegistrationVar4": "health:gp",
            "ProductRegistrationVar7": "news",
            "ProductRegistrationVar8": verified_at,
            "ProductRegistrationVar9": "AB25 1CD",
            "ProductRegistrationVar10": created_at,
        }
        self.assertEqual(expected_params, update_user_profile.params())

    def test_raise_user_token_exception(self):
        verified_at = datetime.datetime.now()
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
        update_user_profile = User(
            "",
            "test@gmail.com",
            "First Name",
            "Last Name",
            "NHS",
            "Developer",
            "health:gp",
            True,
            created_at,
            verified_at,
            "news",
            "AB25 1CD",
            "postcode_region",
        )

        with self.assertRaises(ValueError) as error:
            update_user_profile.params()
        self.assertEqual(str(error.exception), "user_token is empty!")

    def test_user_job_role_mapping(self):
        """Test that User job title with role maps to ProductRegistrationVar4"""
        verified_at = datetime.datetime.now()
        created_at = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")

        update_user_profile = User(
            "token",
            "test@gmail.com",
            "First Name",
            "Last Name",
            "NHS",
            "health:gp",  # job title includes role
            "role",
            True,
            created_at,
            verified_at,
            "news",
            "AB25 1CD",
            "Scotland",  # postcode_region
        )

        params = update_user_profile.params()
        self.assertEqual(params["ProductRegistrationVar4"], "health:gp")
        self.assertEqual(params["ContactVar3"], "Scotland")


class TestUpdatePasswordDataClass(TestCase):
    def test_valid_params(self):
        update_password = UpdatePassword("token", "Test@123")
        expected_params = {"UserToken": "token", "Password": "Test@123"}
        self.assertEqual(expected_params, update_password.params())

    def test_raise_user_token_exception(self):
        update_password = UpdatePassword("", "Test@123")
        with self.assertRaises(ValueError) as error:
            update_password.params()
        self.assertEqual(str(error.exception), "user_token is empty!")

    def test_raise_password_exception(self):
        update_password = UpdatePassword("token", "")
        with self.assertRaises(ValueError) as error:
            update_password.params()
        self.assertEqual(str(error.exception), "password is empty!")

    def test_raise_invalid_password(self):
        update_password = UpdatePassword("token", "test@123")
        with self.assertRaises(PasswordError) as error:
            update_password.params()
        self.assertEqual(
            str(error.exception),
            "Password must be at least 9 characters long, and contain at least 1 number, 1 capital letter, 1 lowercase letter and 1 symbol",
        )


class TestAddressDataClass(TestCase):
    def test_valid_params(self):
        address_lines = {
            "Address1": "address line 1",
            "Address2": "address line 2",
            "Address3": "address line 3",
            "Address4": "address line 4",
            "Address5": "address line 5",
        }
        address = Address("token", address_lines)
        expected_params = {
            "UserToken": "token",
            "Address1": "address line 1",
            "Address2": "address line 2",
            "Address3": "address line 3",
            "Address4": "address line 4",
            "Address5": "address line 5",
        }
        self.assertEqual(expected_params, address.params())

    def test_raise_user_token_exception(self):
        address_lines = {}
        address = Address("", address_lines)

        with self.assertRaises(ValueError) as error:
            address.params()
        self.assertEqual(str(error.exception), "user_token is empty!")


class TestCreateOrderDataClass(TestCase):
    def test_valid_params(self):
        self.maxDiff = None
        order_items = [
            {
                "item_code": "ITEM1",
                "quantity": "2",
                "item_url": "https://test.com/item/1",
                "campaign": "test campaign",
                "image_url": "https://blobstorage.com/image1",
                "title": "Title",
            }
        ]
        order = CreateOrder("token", "1", order_items)
        checkout_items = [
            {
                "ItemCode": "ITEM1",
                "Quantity": "2",
                "Url": "https://test.com/item/1",
                "Campaign": "test campaign",
                "ImageUrl": "https://blobstorage.com/image1",
                "Title": "Title",
            }
        ]
        expected_params = {
            "UserToken": "token",
            "CrcOrderNumber": "1",
            "CheckoutItems": checkout_items,
        }
        self.assertEqual(expected_params, order.params())

    def test_raise_user_token_exception(self):
        order_items = []
        order = CreateOrder("", "1", order_items)

        with self.assertRaises(ValueError) as error:
            order.params()
        self.assertEqual(str(error.exception), "user_token is empty!")

    def test_raise_order_number_exception(self):
        order_items = []
        order = CreateOrder("Token", "", order_items)

        with self.assertRaises(ValueError) as error:
            order.params()
        self.assertEqual(str(error.exception), "order_number is empty!")

    def test_raise_order_items_exception_none(self):
        order_items = None
        order = CreateOrder("Token", "1", order_items)

        with self.assertRaises(ValueError) as error:
            order.params()
        self.assertEqual(str(error.exception), "order_items is empty!")

    def test_raise_order_items_exception_empty(self):
        order_items = []
        order = CreateOrder("Token", "1", order_items)

        with self.assertRaises(ValueError) as error:
            order.params()
        self.assertEqual(str(error.exception), "order_items is empty!")
