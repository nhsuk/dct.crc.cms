from unittest.mock import MagicMock
from django.test import TestCase

from .azure import AzureSearchBackend, AzureSearchRebuilder, AzureSearchException


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


class TestAzureSearchRebuilder(TestCase):
    def setUp(self):
        self.rebuilder = AzureSearchRebuilder("xxx")  # An index that does not exist

    def test_retrieve_current_search_objects(self):
        # Can't seem to mock these objects, so just check we can do a search
        self.rebuilder.azure_search = AzureSearchBackend({})
        result = self.rebuilder.retrieve_current_search_objects()
        # Can't validate the result - could be empty, or not
