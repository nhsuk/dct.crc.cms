import json
from html import escape
from unittest.mock import MagicMock, patch

from django.http import HttpRequest
from django.test import TestCase
from requests import Response, utils

from campaignresourcecentre.campaigns.models import CampaignHubPage, CampaignPage
from campaignresourcecentre.search.azure import (
    AzureSearchBackend,
    AzureSearchRebuilder,
    AzureStorage,
    AzureIndex,
)
from campaignresourcecentre.search.test_data import (
    azure_response,
)


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
        expected = "&$filter=" + utils.quote(
            "((content/resource/objecttype eq 'resource') and (content/resource/TOPIC/any(t: t eq 'SMOKING')))"
        )  # noqa
        facets_filter = self.azure_search._build_query_string_from_filters(filters)
        self.assertEqual(expected, facets_filter)

    def test_create_azure_search_url_and_query(self):
        search_value = "Resource&Campaings"
        fields_queryset = {"objecttype": "resource"}
        facets_queryset = {"TOPIC": "SMOKING"}
        sort_by = "title asc"
        results_per_page = "1000"
        expected = (
            "https://nhsuk-apim-dev-uks.azure-api.net/campaigns-crcv3/crcv3?search="
            + escape(utils.quote("Resource&Campaings"))
            + "&api-version=v1&searchMode=all&$filter="
            + utils.quote(
                "((content/resource/objecttype eq 'resource') and (content/resource/TOPIC/any(t: t eq 'SMOKING')))"
            )
            + "&$orderby=content/resource/title asc&$top=1000"
        )  # noqa
        url = self.azure_search._create_azure_search_url_and_query(
            search_value, fields_queryset, facets_queryset, sort_by, results_per_page
        )
        self.assertEqual(expected, url)

    def test_azure_search_returning_matches(self):
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(azure_response).encode()

        search_value = "Resource"
        fields_queryset = {"objecttype": "resource"}
        facets_queryset = {"TOPIC": "SMOKING"}
        sort_by = "title asc"

        with patch("requests.get", return_value=mock_response):
            actual_data = self.azure_search.azure_search(
                search_value, fields_queryset, facets_queryset, sort_by
            )

        self.assertEqual(azure_response, actual_data["search_content"])
        self.assertTrue(actual_data["ok"])
        self.assertEqual(200, actual_data["code"])

    def test_azure_search_returning_no_matches(self):
        mock_response = Response()
        mock_response.status_code = 200
        search_content = {"value": []}
        mock_response._content = json.dumps(search_content).encode()

        search_value = "Resource"
        fields_queryset = {"objecttype": "resource"}
        facets_queryset = {"TOPIC": "SMOKING"}
        sort_by = "title asc"

        with patch("requests.get", return_value=mock_response):
            actual_data = self.azure_search.azure_search(
                search_value, fields_queryset, facets_queryset, sort_by
            )

        self.assertEqual(search_content, actual_data["search_content"])
        self.assertTrue(actual_data["ok"])
        self.assertEqual(200, actual_data["code"])

    def test_azure_search_returning_no_content(self):
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b""
        search_content = {"value": []}

        search_value = "Resource"
        fields_queryset = {"objecttype": "resource"}
        facets_queryset = {"TOPIC": "SMOKING"}
        sort_by = "title asc"

        with patch("requests.get", return_value=mock_response):
            actual_data = self.azure_search.azure_search(
                search_value, fields_queryset, facets_queryset, sort_by
            )

        self.assertEqual(search_content, actual_data["search_content"])
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
        self.rebuilder.azure_search = AzureSearchBackend({})

    def test_retrieve_current_search_objects(self):
        # Can't seem to mock these objects, so mock the result from the search
        mocked_response = Response()
        mocked_response._content = json.dumps(
            {"value": [MOCKED_RESULT_VALUE, MOCKED_RESULT_VALUE]}
        ).encode()
        mocked_response.status_code = 200

        with patch("requests.get", return_value=mocked_response):
            search_objects = self.rebuilder.retrieve_current_search_objects()

        self.assertEqual(
            repr(search_objects),
            repr(MOCKED_CURRENT_SEARCH_OBJECTS),
        )

    @patch(
        "campaignresourcecentre.search.azure.AzureSearchBackend.delete_search_resource_by_metadata"
    )
    def test_delete_orphan_documents(self, mock_delete):
        orphans = [
            {
                "metadata_storage_path": "path1",
                "content": {"resource": {"object_url": "url1"}},
            },
            {
                "metadata_storage_path": "path2",
                "content": {"resource": {"object_url": "url2"}},
            },
        ]
        self.rebuilder._delete_orphan_documents(orphans)
        self.assertEqual(mock_delete.call_count, 2)
        mock_delete.assert_any_call("path1")
        mock_delete.assert_any_call("path2")

    @patch(
        "campaignresourcecentre.search.azure.AzureSearchBackend.delete_search_resource_by_metadata"
    )
    def test_delete_orphan_documents_empty(self, mock_delete):
        orphans = []
        self.rebuilder._delete_orphan_documents(orphans)
        mock_delete.assert_not_called()


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


class TestAzureIndex(TestCase):
    def setUp(self):
        self.storage_mock = MagicMock()
        self.index = AzureIndex(self.storage_mock)

    def test_is_indexable(self):
        item_mock = MagicMock()
        item_mock.search_indexable.return_value = True
        self.assertTrue(self.index.is_indexable(item_mock))

        item_mock.search_indexable.return_value = False
        self.assertFalse(self.index.is_indexable(item_mock))

        item_mock.search_indexable.side_effect = AttributeError
        self.assertFalse(self.index.is_indexable(item_mock))

    @patch("campaignresourcecentre.search.azure.AzureSearchBackend")
    def test_delete_from_azure_search(self, mock_azure_search_backend):
        item_mock = MagicMock()
        item_mock.search_indexable.return_value = True
        self.index._delete_from_azure_search(item_mock)
        mock_azure_search_backend.return_value.delete_search.assert_called_once_with(
            item_mock
        )

    @patch("campaignresourcecentre.search.azure.get_terms_from_terms_json")
    @patch("campaignresourcecentre.search.azure.get_vocabs_from_terms_json")
    def test_format_taxonomy_for_storage(self, mock_get_vocabs, mock_get_terms):
        mock_get_terms.return_value = ["term1", "term2"]
        mock_get_vocabs.return_value = ["vocab1", "vocab2"]
        taxonomy_data = {"some": "data"}
        expected_output = {"vocabs": ["vocab1", "vocab2"], "terms": ["term1", "term2"]}
        self.assertEqual(
            self.index._format_taxonomy_for_storage(taxonomy_data), expected_output
        )

    @patch("campaignresourcecentre.search.azure.AzureIndex.get_taxonomy_terms")
    @patch(
        "campaignresourcecentre.search.azure.AzureIndex._taxonomy_dict_from_page_terms"
    )
    def test_add_az_index_item(self, mock_taxonomy_dict, mock_get_taxonomy_terms):
        mock_page = MagicMock()
        mock_page.live = True
        mock_page.id = 1
        mock_page.get_az_item.return_value = {"title": "Test Resource"}
        mock_page.taxonomy_json = '{"terms": [{"code": "TERM1"}]}'
        mock_taxonomy_dict.return_value = {"VOCAB1": ["TERM1"]}
        mock_get_taxonomy_terms.return_value = {
            "terms": {"TERM1": {"vocabCode": "VOCAB1", "indexPath": "TERM1"}}
        }

        self.index.add_az_index_item(mock_page)

        self.storage_mock.add_resource.assert_called_once_with(
            1, {"resource": {"title": "Test Resource", "id": 1, "VOCAB1": ["TERM1"]}}
        )

    @patch("campaignresourcecentre.search.azure.AzureIndex.get_taxonomy_terms")
    def test_add_az_index_item_not_live(self, mock_get_taxonomy_terms):
        mock_page = MagicMock()
        mock_page.live = False

        self.index.add_az_index_item(mock_page)
        mock_get_taxonomy_terms.assert_not_called()

    @patch("campaignresourcecentre.search.azure.AzureIndex._delete_from_azure_search")
    def test_delete_item(self, mock_delete_from_azure_search):
        mock_item = MagicMock()
        mock_item.search_indexable.return_value = True

        self.index.delete_item(mock_item)
        mock_delete_from_azure_search.assert_called_once_with(mock_item)
        self.storage_mock.delete_resource.assert_called_once_with(mock_item)

    @patch("campaignresourcecentre.search.azure.AzureIndex._delete_from_azure_search")
    def test_delete_item_not_indexable(self, mock_delete_from_azure_search):
        mock_item = MagicMock()
        mock_item.search_indexable.return_value = False

        result = self.index.delete_item(mock_item)

        self.assertTrue(result)
        mock_delete_from_azure_search.assert_not_called()
        self.storage_mock.delete_resource.assert_not_called()
