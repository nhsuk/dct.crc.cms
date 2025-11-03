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
        self.assertEqual(
            ";".join([m.message for m in messages]),
            "1:C4L301B:Healthy families top tips leaflet;2:C4L301B:Healthy families top tips leaflet;3:C4L301B:Healthy families top tips leaflet;1 duplicated SKU(s)",
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
        self.assertEqual(
            ";".join([m.message for m in messages]),
            "1 duplicated SKU(s);1:C4L301B:Healthy families top tips leaflet;2:C4L301B:Healthy families top tips leaflet",
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

    def test_campaign_name_returns_parent_title(self):
        parent = self.resource_page.get_parent()
        self.assertEqual(self.resource_page.campaign_name, parent.title)

    def test_campaign_name_empty_when_no_parent(self):
        orphan_page = ResourcePage(title="Test", summary="Test", description="Test")
        self.assertEqual(orphan_page.campaign_name, "")

    def test_admin_url_format(self):
        result = self.resource_page.admin_url
        self.assertIn("/crc-admin/pages/", result)
        self.assertIn(f"/{self.resource_page.id}/edit/", result)

    def test_publish_status_live(self):
        self.resource_page.live = True
        self.assertEqual(self.resource_page.publish_status, "Published")

    def test_publish_status_not_live(self):
        self.resource_page.live = False
        self.assertEqual(self.resource_page.publish_status, "Draft")

    def test_first_published_date_formatting(self):
        self.resource_page.first_published_at = datetime(2025, 10, 18, 14, 43, 46)
        self.assertEqual(self.resource_page.first_published_date, "2025-10-18 14:43")

    def test_first_published_date_empty_when_none(self):
        self.resource_page.first_published_at = None
        self.assertEqual(self.resource_page.first_published_date, "")

    def test_last_published_date_formatting(self):
        self.resource_page.last_published_at = datetime(2025, 11, 3, 10, 30, 0)
        self.assertEqual(self.resource_page.last_published_date, "2025-11-03 10:30")

    def test_last_published_date_empty_when_none(self):
        self.resource_page.last_published_at = None
        self.assertEqual(self.resource_page.last_published_date, "")

    def test_taxonomy_properties(self):
        self.resource_page.taxonomy_json = json.dumps(
            [
                {"code": "EATING", "label": "Eating well"},
                {"code": "PARENTSANDCHILDREN", "label": "Parents and children"},
            ]
        )
        self.resource_page.save_revision().publish()
        self.resource_page = ResourcePage.objects.get(id=self.resource_page.id)
        self.assertEqual(self.resource_page.topics, "Eating well")
        self.assertEqual(self.resource_page.target_audience, "Parents and children")
        self.assertEqual(self.resource_page.language, "")
        self.assertEqual(self.resource_page.profession, "")

    def test_taxonomy_properties_empty_when_no_json(self):
        self.resource_page.taxonomy_json = None
        self.assertEqual(self.resource_page.topics, "")
        self.assertEqual(self.resource_page.target_audience, "")
        self.assertEqual(self.resource_page.language, "")
        self.assertEqual(self.resource_page.profession, "")
        self.assertEqual(self.resource_page.alternative_format, "")
        self.assertEqual(self.resource_page.taxonomy_resource_type, "")

    def test_objecttype(self):
        self.assertEqual(self.resource_page.objecttype(), "resource")
