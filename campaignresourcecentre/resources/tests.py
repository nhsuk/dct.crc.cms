import json
from uuid import uuid4
from unittest import skip, skipIf

from django.contrib import admin
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import ValidationError
from django.template import engines
from django.test import TestCase
from django.test import RequestFactory

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.core.preparetestdata import PrepareTestData
from .models import ResourcePage, ResourceItem
from .admin import ResourcePageAdmin, ResourceItemAdmin
from datetime import datetime


class TestResourceSkusProperty(TestCase):
    def setUp(self):
        test_data = PrepareTestData()
        self.resource_page = test_data.resource_page
        self.resource_item = test_data.resource_item

    def test_resource_skus_returns_sku(self):
        self.assertEqual(self.resource_page.resource_skus, "C4L301B")

    def test_resource_skus_returns_empty_string_when_no_skus(self):
        self.resource_item.sku = ""
        self.resource_item.save()
        self.assertEqual(self.resource_page.resource_skus, "")

    def test_resource_skus_returns_comma_separated_for_multiple(self):
        ResourceItem.objects.create(
            resource_page=self.resource_page,
            title="Second item",
            can_order=True,
            sku="C4L302A",
            maximum_order_quantity=500,
            sort_order=1,
        )
        result = self.resource_page.resource_skus
        self.assertIn("C4L301B", result)
        self.assertIn("C4L302A", result)
        self.assertIn(", ", result)

    def test_resource_skus_excludes_blank_skus(self):
        ResourceItem.objects.create(
            resource_page=self.resource_page,
            title="No SKU item",
            can_download=True,
            can_order=False,
            sku="",
            sort_order=1,
        )
        self.assertEqual(self.resource_page.resource_skus, "C4L301B")


class TestResourceOrderableProperty(TestCase):
    def setUp(self):
        test_data = PrepareTestData()
        self.resource_page = test_data.resource_page
        self.resource_item = test_data.resource_item

    def test_resource_orderable_returns_yes_when_orderable(self):
        self.assertEqual(self.resource_page.resource_orderable, "Yes")

    def test_resource_orderable_returns_no_when_not_orderable(self):
        self.resource_item.can_order = False
        self.resource_item.save()
        self.assertEqual(self.resource_page.resource_orderable, "No")

    def test_resource_orderable_returns_no_when_no_items(self):
        self.resource_page.resource_items.all().delete()
        self.assertEqual(self.resource_page.resource_orderable, "No")

    def test_resource_orderable_yes_if_any_item_orderable(self):
        self.resource_item.can_order = False
        self.resource_item.save()
        ResourceItem.objects.create(
            resource_page=self.resource_page,
            title="Orderable item",
            can_order=True,
            sku="SKU123",
            maximum_order_quantity=10,
            sort_order=1,
        )
        self.assertEqual(self.resource_page.resource_orderable, "Yes")


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
            taxonomy_json=json.dumps([{"code": "CANCER", "label": "Cancer"}]),
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
            taxonomy_json=json.dumps([{"code": "COVID", "label": "Coronavirus"}]),
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
            taxonomy_json=json.dumps([{"code": "CANCER", "label": "Cancer"}]),
        )
        self.campaign_page.add_child(instance=child_campaign)
        child_campaign.save()

        nested_resource = ResourcePage(
            title="Nested Resource",
            summary="Test summary",
            description="Test description",
            taxonomy_json=json.dumps([{"code": "COVID", "label": "Coronavirus"}]),
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

    def test_topics_returns_topic_labels(self):
        self.resource_page.taxonomy_json = json.dumps(
            [
                {"code": "EATING", "label": "Eating well"},
                {"code": "ADULTS", "label": "Adults"},
            ]
        )
        self.assertIn("Eating well", self.resource_page.topics)

    def test_all_taxonomy_tags_includes_multiple_categories(self):
        self.resource_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "ADULTS", "label": "Adults"},
                {"code": "ARABIC", "label": "Arabic"},
            ]
        )
        result = self.resource_page.all_taxonomy_tags
        self.assertIn("Cancer", result)
        self.assertIn("Adults", result)
        self.assertIn("Arabic", result)

    def test_objecttype(self):
        self.assertEqual(self.resource_page.objecttype(), "resource")


class TestRemoveTopicFilterTagRegression(TestCase):
    def _render_topic_tag(self, code):
        template = engines["django"].get_template(
            "molecules/search-result/refresh-search.html"
        )
        return template.render(
            {
                "count": 1,
                "search_results": [],
                "taxonomies": [
                    {
                        "label": "Health topics",
                        "code": "TOPIC",
                        "type": "vocabulary",
                        "children": [
                            {
                                "label": "test topic",
                                "code": code,
                                "type": "term",
                                "children": [],
                            }
                        ],
                    }
                ],
                "facets_queryset": {"TOPIC": [code]},
                "sort": "relevant",
            }
        )

    def test_lowercase_topic_tag_button_has_parent_topic_attribute(self):
        html = self._render_topic_tag("testtopic")
        self.assertIn(
            '<button class="taxonomy-tags__child" value="testtopic-input" parent="TOPIC"',
            html,
        )

    def test_uppercase_topic_tag_button_has_parent_topic_attribute(self):
        html = self._render_topic_tag("TESTTOPIC")
        self.assertIn(
            '<button class="taxonomy-tags__child" value="TESTTOPIC-input" parent="TOPIC"',
            html,
        )
