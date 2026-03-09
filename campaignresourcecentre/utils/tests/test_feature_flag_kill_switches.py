from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Site

from campaignresourcecentre.core.preparetestdata import PrepareTestData
from campaignresourcecentre.utils.models import FeatureFlags


class FeatureFlagKillSwitchTests(TestCase):
    def setUp(self):
        test_data = PrepareTestData()
        self.resource_page = test_data.resource_page
        self.default_site = Site.objects.get(is_default_site=True)

    def _set_flags(self, disable_ordering_and_checkout=False, disable_order_history=False):
        FeatureFlags.objects.update_or_create(
            site=self.default_site,
            defaults={
                "disable_ordering_and_checkout": disable_ordering_and_checkout,
                "disable_order_history": disable_order_history,
            },
        )

    def _set_logged_in_session(self):
        session = self.client.session
        session["ParagonUser"] = "token"
        session["Verified"] = "True"
        session["UserDetails"] = {"ProductRegistrationVar1": "uber"}
        session.save()

    def test_basket_and_checkout_endpoints_return_404_when_disabled(self):
        self._set_flags(disable_ordering_and_checkout=True)
        self._set_logged_in_session()

        basket_get = self.client.get("/baskets/view_basket/")
        basket_post = self.client.post("/baskets/add_item/", {})
        order_summary = self.client.get("/orders/summary/")
        order_address = self.client.get("/orders/address/edit/")
        place_order = self.client.post("/orders/place_order/", {})

        self.assertEqual(basket_get.status_code, 404)
        self.assertEqual(basket_post.status_code, 404)
        self.assertEqual(order_summary.status_code, 404)
        self.assertEqual(order_address.status_code, 404)
        self.assertEqual(place_order.status_code, 404)

    def test_order_history_endpoint_returns_404_when_disabled(self):
        self._set_flags(disable_order_history=True)
        self._set_logged_in_session()

        response = self.client.get("/account/orders/")

        self.assertEqual(response.status_code, 404)

    @patch("campaignresourcecentre.paragon_users.views.Client.get_user_profile")
    def test_account_hides_order_history_link_when_disabled(self, mock_get_user_profile):
        mock_get_user_profile.return_value = {
            "content": {
                "FirstName": "Test",
                "LastName": "User",
                "EmailAddress": "test@example.com",
                "ProductRegistrationVar3": "Org",
                "ProductRegistrationVar4": "admin",
                "ProductRegistrationVar9": "WC1 2AA|region.london",
                "ProductRegistrationVar1": "uber",
            }
        }

        self._set_flags(disable_order_history=True)
        self._set_logged_in_session()

        response = self.client.get("/account/")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Order history")

    def test_session_summary_hides_basket_when_ordering_disabled(self):
        self._set_flags(disable_ordering_and_checkout=True)

        response = self.client.get("/session/summary")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "nhsuk-header__account-item-basket")

    def test_resource_page_hides_order_form_when_ordering_disabled(self):
        self._set_flags(disable_ordering_and_checkout=True)
        self._set_logged_in_session()

        response = self.client.get(self.resource_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Add to basket")

    def test_resource_page_shows_order_form_when_ordering_enabled(self):
        self._set_flags(disable_ordering_and_checkout=False)
        self._set_logged_in_session()

        response = self.client.get(self.resource_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add to basket")

    def test_resource_item_cannot_be_orderable_when_ordering_disabled(self):
        self._set_flags(disable_ordering_and_checkout=True)
        resource_item = self.resource_page.resource_items.first()

        with self.assertRaises(ValidationError) as context:
            resource_item.clean()

        self.assertIn("can_order", context.exception.message_dict)
