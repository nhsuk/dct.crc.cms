import json
from django.contrib import admin
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase
from django.test import RequestFactory

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.core.preparetestdata import PrepareTestData
from .models import ResourcePage, ResourceItem
from .admin import ResourcePageAdmin, ResourceItemAdmin

# Mock a request object and user with all permissions


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()


def new_request():
    request = request_factory.get("/admin")
    request.user = MockSuperUser()

    # So we can test using messsages
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


class AdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        td = PrepareTestData()
        cls.resource_page = td.resource_page
        cls.resource_item = td.resource_item
        cls.campaign_page = td.campaign_page


class TestResourcePageAdmin(AdminTestCase):
    def test_list_display(self):
        self.assertEqual(
            ResourcePageAdmin.list_display,
            ("id", "live", "has_unpublished_changes", "title", "url"),
        )

    def test_display(self):
        expected_fields = [field.name for field in ResourcePage._meta.get_fields()] + [
            "search_json"
        ]
        self.assertEqual(ResourcePageAdmin.display, expected_fields)

    def test_search_fields(self):
        expected_search_fields = ["title", "description", "summary"]
        self.assertEqual(ResourcePageAdmin.search_fields, expected_search_fields)

    def test_azure_search_json(self):
        admin_instance = ResourcePageAdmin(ResourcePage, admin.site)
        obj = self.resource_page
        obj.search_indexable = True
        result = admin_instance.azure_search_json(obj)
        expected_result = json.dumps(obj.get_az_item(), indent=4, sort_keys=True)
        self.assertEqual(result, expected_result)


class TestResourceItemAdmin(AdminTestCase):
    def setUp(self):
        self.admin = ResourceItemAdmin(ResourceItem, admin.site)
        self.request = new_request()

    def test_list_display(self):
        expected_list_display = (
            "id",
            "campaign_title",
            "sku",
            "title",
            "can_order",
            "maximum_order_quantity",
            "image",
            "document",
        )
        self.assertEqual(ResourceItemAdmin.list_display, expected_list_display)

    def test_campaign_title(self):
        admin_instance = ResourceItemAdmin(ResourceItem, admin.site)
        result = admin_instance.campaign_title(self.resource_item)
        expected_result = "Change4Life"
        self.assertEqual(result, expected_result)

    def test_identifyDuplicatedSKUs(self):
        self.admin.identifyDuplicatedSKUs(self.request, [])
        messages = get_messages(self.request)
        self.assertEqual(";".join([m.message for m in messages]), "No duplicated SKUs")

    def test_identifyWithinCampaignDuplicatedSKUs(self):
        self.admin.identifyWithinCampaignDuplicatedSKUs(self.request, [])
        messages = get_messages(self.request)
        self.assertEqual(";".join([m.message for m in messages]), "No duplicated SKUs")
