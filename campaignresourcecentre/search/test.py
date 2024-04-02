import json
from unittest.mock import MagicMock, patch

from django.test import TestCase

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
