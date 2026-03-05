import json
from datetime import datetime

from django.test import TestCase

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.core.preparetestdata import PrepareTestData
from campaignresourcecentre.reports.views import (
    CampaignResourceFilterSet,
    CampaignResourceOrderableFilterSet,
    get_all_taxonomy_terms,
)
from campaignresourcecentre.resources.models import ResourcePage


class TestCampaignResourceFilterSet(TestCase):
    def setUp(self):
        test_data = PrepareTestData()
        self.resource_page = test_data.resource_page
        self.campaign_page = test_data.campaign_page
        self.resource_page.taxonomy_json = json.dumps(
            [{"code": "ADULTS", "label": "Adults"}, {"code": "FLU", "label": "Flu"}]
        )
        self.resource_page.save()

    def test_get_all_taxonomy_terms_returns_sorted_list(self):
        terms = get_all_taxonomy_terms()
        labels = [term[1] for term in terms]

        self.assertEqual(labels, sorted(labels))

    def test_filter_taxonomy_with_no_value(self):
        filterset = CampaignResourceFilterSet()
        queryset = ResourcePage.objects.all()
        result = filterset.filter_taxonomy(queryset, "taxonomy", [])

        self.assertEqual(list(result), list(queryset))

    def test_filter_taxonomy_with_single_matching_term(self):
        filterset = CampaignResourceFilterSet()
        result = filterset.filter_taxonomy(
            ResourcePage.objects.all(), "taxonomy", ["ADULTS"]
        )

        self.assertIn(self.resource_page, result)

    def test_filter_taxonomy_with_multiple_terms_all_match(self):
        filterset = CampaignResourceFilterSet()
        result = filterset.filter_taxonomy(
            ResourcePage.objects.all(), "taxonomy", ["ADULTS", "FLU"]
        )

        self.assertIn(self.resource_page, result)

    def test_filter_taxonomy_with_multiple_terms_partial_match(self):
        self.resource_page.taxonomy_json = json.dumps(
            [
                {"code": "ADULTS", "label": "Adults"},
                {"code": "CANCER", "label": "Cancer"},
            ]
        )
        self.resource_page.save()

        filterset = CampaignResourceFilterSet()
        result = filterset.filter_taxonomy(
            ResourcePage.objects.all(), "taxonomy", ["ADULTS", "FLU"]
        )

        self.assertNotIn(self.resource_page, result)

    def test_filter_campaign_with_no_value(self):
        filterset = CampaignResourceFilterSet()
        queryset = ResourcePage.objects.all()
        result = filterset.filter_campaign(queryset, "campaign", [])

        self.assertEqual(list(result), list(queryset))

    def test_filter_campaign_with_single_campaign(self):
        filterset = CampaignResourceFilterSet()
        result = filterset.filter_campaign(
            ResourcePage.objects.all(), "campaign", [self.campaign_page]
        )

        self.assertIn(self.resource_page, result)

    def test_filter_campaign_with_multiple_campaigns(self):
        sub_campaign = CampaignPage(
            title="Sub Campaign",
            summary="A sub campaign",
            description="Nested campaign",
            image=self.campaign_page.image,
            taxonomy_json=json.dumps([{"code": "CANCER", "label": "Cancer"}]),
        )
        self.campaign_page.add_child(instance=sub_campaign)
        sub_campaign.save_revision().publish()

        nested_resource = ResourcePage(
            title="Nested Resource",
            summary="A resource",
            description="Test resource",
            permission_role="all",
            taxonomy_json=json.dumps([{"code": "COVID", "label": "Coronavirus"}]),
        )
        sub_campaign.add_child(instance=nested_resource)
        nested_resource.save_revision().publish()

        filterset = CampaignResourceFilterSet()
        result = filterset.filter_campaign(
            ResourcePage.objects.all(), "campaign", [self.campaign_page, sub_campaign]
        )

        self.assertIn(nested_resource, result)
        self.assertNotIn(self.resource_page, result)


class TestCampaignResourceOrderableFilterSet(TestCase):
    def setUp(self):
        test_data = PrepareTestData()
        self.resource_page = test_data.resource_page
        self.campaign_page = test_data.campaign_page
        self.resource_item = test_data.resource_item

    def test_filter_orderable_with_no_value(self):
        filterset = CampaignResourceOrderableFilterSet()
        queryset = ResourcePage.objects.all()
        result = filterset.filter_orderable(queryset, "orderable", "")
        self.assertEqual(list(result), list(queryset))

    def test_filter_orderable_yes_returns_orderable_resources(self):
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_orderable(
            ResourcePage.objects.all(), "orderable", "yes"
        )
        self.assertIn(self.resource_page, result)

    def test_filter_orderable_no_excludes_orderable_resources(self):
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_orderable(
            ResourcePage.objects.all(), "orderable", "no"
        )
        self.assertNotIn(self.resource_page, result)

    def test_filter_orderable_yes_excludes_non_orderable(self):
        self.resource_item.can_order = False
        self.resource_item.save()
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_orderable(
            ResourcePage.objects.all(), "orderable", "yes"
        )
        self.assertNotIn(self.resource_page, result)

    def test_filter_orderable_no_returns_non_orderable(self):
        self.resource_item.can_order = False
        self.resource_item.save()
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_orderable(
            ResourcePage.objects.all(), "orderable", "no"
        )
        self.assertIn(self.resource_page, result)

    def test_filter_status_with_no_value(self):
        filterset = CampaignResourceOrderableFilterSet()
        queryset = ResourcePage.objects.all()
        result = filterset.filter_status(queryset, "status", "")
        self.assertEqual(list(result), list(queryset))

    def test_filter_status_live_returns_published(self):
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_status(ResourcePage.objects.all(), "status", "live")
        self.assertIn(self.resource_page, result)

    def test_filter_status_draft_excludes_published(self):
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_status(ResourcePage.objects.all(), "status", "draft")
        self.assertNotIn(self.resource_page, result)

    def test_filter_campaign_with_no_value(self):
        filterset = CampaignResourceOrderableFilterSet()
        queryset = ResourcePage.objects.all()
        result = filterset.filter_campaign(queryset, "campaign", [])
        self.assertEqual(list(result), list(queryset))

    def test_filter_campaign_with_matching_campaign(self):
        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_campaign(
            ResourcePage.objects.all(), "campaign", [self.campaign_page]
        )
        self.assertIn(self.resource_page, result)

    def test_filter_campaign_with_multiple_campaigns(self):
        hub = self.campaign_page.get_parent()
        second_campaign = CampaignPage(
            title="Second Campaign",
            summary="Summary",
            description="Description",
            show_in_menus=True,
        )
        hub.add_child(instance=second_campaign)
        second_campaign.save_revision().publish()

        second_resource = ResourcePage(
            title="Second Resource",
            summary="Summary",
            description="Description",
            permission_role="all",
        )
        second_campaign.add_child(instance=second_resource)
        second_resource.save_revision().publish()

        filterset = CampaignResourceOrderableFilterSet()
        result = filterset.filter_campaign(
            ResourcePage.objects.all(),
            "campaign",
            [self.campaign_page, second_campaign],
        )
        self.assertIn(self.resource_page, result)
        self.assertIn(second_resource, result)
