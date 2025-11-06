import json
from uuid import uuid4
from unittest import skip, skipIf

from django.contrib import admin
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import RequestFactory

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.core.preparetestdata import PrepareTestData
from .models import ResourcePage, ResourceItem
from .admin import ResourcePageAdmin, ResourceItemAdmin
from datetime import datetime

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
    def prepareTestData(self):
        td = PrepareTestData()
        self.resource_page = td.resource_page
        self.resource_item = td.resource_item
        self.campaign_page = td.campaign_page
        self.campaign_hub_page = td.campaign_hub_page


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
        self.prepareTestData()
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

    def test_prepared_data_operations(self):
        self.prepareTestData()  # These tests rely on the structure of the test data and make a specific sequence of changes
        self.internal_test_can_update_existing_item()
        self.internal_test_cannot_save_with_null_sku()
        self.internal_test_identifyDuplicatedSKUs_when_none()
        self.request = new_request()  # Clear messages
        self.internal_test_identifyWithinCampaignDuplicatedSKUs_when_none()
        self.request = new_request()
        # Verify there is one between campaign duplicate
        self.internal_test_identifyDuplicatedSKUs_when_one()
        self.request = new_request()
        # Create a within-campaign duplicate
        self.resource_item.pk = None
        self.resource_item.save()
        # Verify now one within campaign duplicates
        self.internal_test_identifyWithinCampaignDuplicatedSKUs_when_one()
        self.request = new_request()

    def internal_test_identifyDuplicatedSKUs_when_none(self):
        self.admin.identifyDuplicatedSKUs(self.request, [])
        messages = get_messages(self.request)
        self.assertEqual(";".join([m.message for m in messages]), "No duplicated SKUs")

    def internal_test_identifyWithinCampaignDuplicatedSKUs_when_none(self):
        self.admin.identifyWithinCampaignDuplicatedSKUs(self.request, [])
        messages = get_messages(self.request)
        self.assertEqual(";".join([m.message for m in messages]), "No duplicated SKUs")

    def internal_test_identifyWithinCampaignDuplicatedSKUs_when_one(self):
        self.admin.identifyWithinCampaignDuplicatedSKUs(self.request, [])
        messages = get_messages(self.request)
        message_text = ";".join([m.message for m in messages])
        self.assertIn("1 duplicated SKU(s)", message_text)
        self.assertEqual(
            message_text.count("C4L301B:Healthy families top tips leaflet"), 3
        )

    def internal_test_identifyDuplicatedSKUs_when_one(self):
        new_campaign = CampaignPage(
            title=uuid4(),
            summary=uuid4(),
            description=uuid4(),
            image=self.campaign_page.image,
            show_in_menus=True,
            last_published_at=self.campaign_page.last_reviewed,
            slug=uuid4(),
            translation_key=uuid4(),
        )
        self.campaign_hub_page.specific.add_child(instance=new_campaign)
        new_campaign.save()
        new_campaign.refresh_from_db()
        # Create a new resource in this new campaign
        new_resource_page = ResourcePage(
            title=uuid4(),
            summary=uuid4(),
            description=uuid4(),
            permission_role=self.resource_page.permission_role,
            last_published_at=self.resource_page.last_published_at,
        )
        new_campaign.specific.add_child(instance=new_resource_page)
        new_resource_page.save()
        new_resource_page.refresh_from_db()

        # Create a new resource item with the same SKU in this new resource
        self.resource_item.pk = None
        self.resource_item.resource_page = new_resource_page

        # This should pass cleaning
        self.resource_item.clean()
        self.resource_item.save()

        self.admin.identifyDuplicatedSKUs(self.request, [])
        messages = get_messages(self.request)
        message_text = ";".join([m.message for m in messages])
        self.assertIn("1 duplicated SKU(s)", message_text)
        self.assertEqual(
            message_text.count("C4L301B:Healthy families top tips leaflet"), 2
        )

    def internal_test_can_update_existing_item(self):
        self.resource_item.clean()

    def internal_test_cannot_save_with_null_sku(self):
        sku = self.resource_item.sku
        self.resource_item.sku = None
        with self.assertRaises(ValidationError) as context:
            self.resource_item.clean()
        self.assertEqual({"sku": ["Please enter a SKU"]}, context.exception.args[0])
        self.resource_item.sku = sku


class TestResourcePageProperties(AdminTestCase):
    def setUp(self):
        self.prepareTestData()

    def test_parent_campaign_chain_single_level(self):
        parent = self.resource_page.get_parent()
        result = self.resource_page.parent_campaign_chain
        self.assertEqual(result, parent.title)

    def test_parent_campaign_chain_nested_campaigns(self):
        child_campaign = CampaignPage(
            title="Child Campaign",
            summary="Child summary",
            description="Child description",
            image=self.campaign_page.image,
        )
        self.campaign_page.add_child(instance=child_campaign)
        child_campaign.save()

        nested_resource = ResourcePage(
            title="Nested Resource",
            summary="Test summary",
            description="Test description",
        )
        child_campaign.add_child(instance=nested_resource)
        nested_resource.save()

        result = nested_resource.parent_campaign_chain
        self.assertEqual(result, f"{self.campaign_page.title} > {child_campaign.title}")

    def test_parent_campaign_chain_empty_when_no_parent(self):
        orphan_page = ResourcePage(title="Test", summary="Test", description="Test")
        self.assertEqual(orphan_page.parent_campaign_chain, "")

    def test_taxonomy_properties_exist(self):
        self.assertIsInstance(self.resource_page.topics, str)
        self.assertIsInstance(self.resource_page.target_audience, str)
        self.assertIsInstance(self.resource_page.language, str)
        self.assertIsInstance(self.resource_page.profession, str)
        self.assertIsInstance(self.resource_page.alternative_format, str)
        self.assertIsInstance(self.resource_page.taxonomy_resource_type, str)

    def test_taxonomy_properties_empty_when_no_json(self):
        self.resource_page.taxonomy_json = None
        self.assertEqual(self.resource_page.topics, "")
        self.assertEqual(self.resource_page.target_audience, "")
        self.assertEqual(self.resource_page.language, "")
        self.assertEqual(self.resource_page.profession, "")
        self.assertEqual(self.resource_page.alternative_format, "")
        self.assertEqual(self.resource_page.taxonomy_resource_type, "")

    def test_all_taxonomy_tags_returns_string(self):
        result = self.resource_page.all_taxonomy_tags
        self.assertIsInstance(result, str)

    def test_objecttype(self):
        self.assertEqual(self.resource_page.objecttype(), "resource")
