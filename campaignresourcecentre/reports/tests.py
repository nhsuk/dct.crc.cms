import json
from datetime import datetime

from django.test import TransactionTestCase

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.core.preparetestdata import PrepareTestData
from campaignresourcecentre.reports.views import (
    CampaignResourceFilterSet,
    get_all_taxonomy_terms,
)
from campaignresourcecentre.resources.models import ResourcePage


class TestCampaignResourceFilterSet(TransactionTestCase):
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
            [{"code": "ADULTS", "label": "Adults"}]
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
        )
        self.campaign_page.add_child(instance=sub_campaign)
        sub_campaign.save_revision().publish()

        nested_resource = ResourcePage(
            title="Nested Resource",
            summary="A resource",
            description="Test resource",
            permission_role="all",
        )
        sub_campaign.add_child(instance=nested_resource)
        nested_resource.save_revision().publish()

        filterset = CampaignResourceFilterSet()
        result = filterset.filter_campaign(
            ResourcePage.objects.all(), "campaign", [self.campaign_page, sub_campaign]
        )

        self.assertIn(nested_resource, result)
        self.assertNotIn(self.resource_page, result)
