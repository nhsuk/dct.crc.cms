import json
from unittest.mock import MagicMock, patch
from requests import Response

from django.test import TestCase
from django.http import HttpRequest

from .azure import (
    AzureSearchBackend,
    AzureSearchRebuilder,
    AzureSearchException,
    AzureStorage,
    AzureIndex,
)

from campaignresourcecentre.core.management.commands.searchorphans import (
    process_orphans,
)
from campaignresourcecentre.campaigns.models import CampaignHubPage, CampaignPage


class TestAzureSearchBackend(TestCase):
    def setUp(self):
        self.azure_search = AzureSearchBackend({})

    def test_get_filters_from_facets(self):
        facets_queryset = {"TOPIC": "SMOKING"}
        expected = ["(content/resource/TOPIC/any(t: t eq 'SMOKING'))"]
        facets_filter = self.azure_search._get_filters_from_facets(facets_queryset)
        self.assertEqual(expected, facets_filter)

    def test_get_filters_from_fields(self):
        fields_queryset = {"objecttype": "resource"}
        expected = ["(content/resource/objecttype eq 'resource')"]
        facets_filter = self.azure_search._get_filters_from_fields(fields_queryset)
        self.assertEqual(expected, facets_filter)

    def test_build_query_string_from_filters(self):
        filters = [
            "(content/resource/objecttype eq 'resource')",
            "(content/resource/TOPIC/any(t: t eq 'SMOKING'))",
        ]
        expected = "&$filter=((content/resource/objecttype eq 'resource') and (content/resource/TOPIC/any(t: t eq 'SMOKING')))"  # noqa
        facets_filter = self.azure_search._build_query_string_from_filters(filters)
        self.assertEqual(expected, facets_filter)

    def test_create_azure_search_url_and_query(self):
        search_value = "Resource"
        fields_queryset = {"objecttype": "resource"}
        facets_queryset = {"TOPIC": "SMOKING"}
        sort_by = "title asc"
        results_per_page = "1000"
        expected = "https://nhsuk-apim-dev-uks.azure-api.net/campaigns-crcv3/crcv3?search=Resource&api-version=v1&searchMode=all&$filter=((content/resource/objecttype eq 'resource') and (content/resource/TOPIC/any(t: t eq 'SMOKING')))&$orderby=content/resource/title asc&$top=1000"  # noqa
        url = self.azure_search._create_azure_search_url_and_query(
            search_value, fields_queryset, facets_queryset, sort_by, results_per_page
        )
        self.assertEqual(expected, url)

    @patch("requests.get")
    def test_azure_search_returning_matches(self, mock_get):
        mock_response = Response()
        with open(
            "./campaignresourcecentre/search/test_sample_azure_response.json"
        ) as f:
            mock_response.status_code = 200
            mock_response._content = f.read().encode()
            mock_matches_obj = json.load(f)

        mock_get.return_value = mock_response

        search_value = "Resource"
        fields_queryset = {"objecttype": "resource"}
        facets_queryset = {"TOPIC": "SMOKING"}
        sort_by = "title asc"
        actual_data = self.azure_search.azure_search(
            search_value, fields_queryset, facets_queryset, sort_by
        )

        self.assertEqual(mock_matches_obj, actual_data["search_content"])
        self.assertTrue(actual_data["ok"])
        self.assertEqual(200, actual_data["code"])


DUMMY_URL = "https://example.com/something-to-search-for"
MOCKED_RESULT_VALUE = {
    "content": {
        "resource": {
            "object_url": DUMMY_URL,
            "objecttype": "resource",
        }
    }
}

MOCKED_CURRENT_SEARCH_OBJECTS = {
    DUMMY_URL: [
        MOCKED_RESULT_VALUE,
        MOCKED_RESULT_VALUE,
    ]
}


MOCKED_ORPHANS_RESULT = [
    (
        f"resource {DUMMY_URL}",
        {
            "content": {
                "resource": {
                    "object_url": DUMMY_URL,
                    "objecttype": "resource",
                }
            }
        },
    ),
    (
        f"resource {DUMMY_URL}",
        {
            "content": {
                "resource": {
                    "object_url": DUMMY_URL,
                    "objecttype": "resource",
                }
            }
        },
    ),
]


class TestAzureSearchRebuilder(TestCase):
    def setUp(self):
        self.storage = AzureStorage()
        self.backend = AzureSearchBackend({})
        self.index = AzureIndex(self.storage)
        self.rebuilder = AzureSearchRebuilder(self.index)

    def test_retrieve_current_search_objects(self):
        # Can't seem to mock these objects, so mock the result from the search
        self.rebuilder.azure_search = AzureSearchBackend({})
        mocked_response = MagicMock()
        mocked_response.content = json.dumps(
            {"value": [MOCKED_RESULT_VALUE, MOCKED_RESULT_VALUE]}
        )
        mocked_response.json().return_value = {
            "value": [MOCKED_RESULT_VALUE, MOCKED_RESULT_VALUE]
        }
        mocked_response.ok = True
        mocked_response.status_code = 200

        with patch("requests.get", return_value=mocked_response):
            search_objects = self.rebuilder.retrieve_current_search_objects()
        self.assertEqual(
            repr(search_objects),
            repr(MOCKED_CURRENT_SEARCH_OBJECTS),
        )

    def test_process_orphans(self):
        results = []

        def mocked_process_dup(label, orphan):
            results.append((label, orphan))

        process_orphans(MOCKED_CURRENT_SEARCH_OBJECTS, None, mocked_process_dup)
        self.assertEqual(
            repr(results),
            repr(MOCKED_ORPHANS_RESULT),
        )


class TestDatabaseSearch(TestCase):
    def setUp(self):
        self.campaign_hub_page = CampaignHubPage()
        self.mock_campaigns = [
            MagicMock(
                spec=CampaignPage,
                id=1,
                listing_title="Campaign 1",
                listing_image="Image1.jpg",
                summary="Summary 1",
                listing_summary="Listing Summary 1",
                url="/campaign/1/",
                taxonomy_json=json.dumps([{"code": "FLU"}]),
            ),
            MagicMock(
                spec=CampaignPage,
                id=2,
                listing_title="Campaign 2",
                listing_image="Image2.jpg",
                summary="Summary 2",
                listing_summary="Listing Summary 2",
                url="/campaign/2/",
                taxonomy_json=json.dumps([{"code": "FLU"}]),
            ),
            MagicMock(
                spec=CampaignPage,
                id=3,
                listing_title="Campaign 3",
                listing_image="Image3.jpg",
                summary="Summary 3",
                listing_summary="Listing Summary 3",
                url="/campaign/3/",
                taxonomy_json=json.dumps([{"code": "CANCER"}]),
            ),
        ]
        self.expected_mock_campaigns_data = [
            {
                "title": mock.listing_title,
                "summary": mock.summary,
                "image": mock.listing_image,
                "listing_summary": mock.listing_summary,
                "url": mock.url,
            }
            for mock in self.mock_campaigns
        ]

    @patch("campaignresourcecentre.campaigns.models.CampaignPage.objects.live")
    def test_from_database_filter_all(self, mock_live):
        mock_queryset = MagicMock()
        mock_queryset.public().child_of().order_by.return_value = self.mock_campaigns
        mock_live.return_value = mock_queryset

        request = HttpRequest()
        request.GET["topic"] = "ALL"
        request.GET["sort"] = "recommended"

        actual_data = self.campaign_hub_page.from_database(request)
        self.assertEqual(self.expected_mock_campaigns_data, actual_data)

    @patch("campaignresourcecentre.campaigns.models.CampaignPage.objects.live")
    def test_from_database_filter_specific_topic(self, mock_live):
        mock_live().public().child_of().order_by.return_value = self.mock_campaigns

        request = HttpRequest()
        request.GET["topic"] = "CANCER"

        expected_data = [
            {
                "title": "Campaign 3",
                "summary": "Summary 3",
                "image": "Image3.jpg",
                "listing_summary": "Listing Summary 3",
                "url": "/campaign/3/",
            }
        ]

        actual_data = self.campaign_hub_page.from_database(request)
        self.assertEqual(expected_data, actual_data)

    @patch("campaignresourcecentre.campaigns.models.CampaignPage.objects.live")
    @patch("campaignresourcecentre.campaigns.models.logger")
    def test_from_database_invalid_json(self, mock_logger, mock_live):
        self.mock_campaigns.append(
            MagicMock(
                spec=CampaignPage,
                id=4,
                listing_title="Invalid JSON Campaign",
                listing_image="ImageInvalid.jpg",
                listing_summary="Invalid JSON Summary",
                url="/campaign/invalid/",
                taxonomy_json="",
            )
        )

        mock_live().public().child_of().order_by.return_value = self.mock_campaigns

        request = HttpRequest()
        request.GET["topic"] = "ALL"

        self.campaign_hub_page.from_database(request)

        mock_logger.error.assert_called()
