import json
import re
import logging
import requests

from django.conf import settings
from django.db.models.query import QuerySet

from wagtail.core.models import Page, PageQuerySet

from wagtailreacttaxonomy.models import (
    TaxonomyTerms,
    get_terms_from_terms_json,
    get_vocabs_from_terms_json,
)
from wagtail.search.backends.base import BaseSearchBackend, BaseSearchResults, EmptySearchResults
from wagtail.search.query import PlainText

from campaignresourcecentre.azurestore.utils import AzureStorage, CacheStorage

logger = logging.getLogger(__name__)

def slugpages(slug, site=None):
    """
    Returns a QuerySet of pages having the given slug.
    First tries to find the page(s) on a specified site.
    If that fails or no site is specified, then returns the pages
    matching the slug on any site.
    """
  
    if site is None:
        pages = None
    else:
        pages = Page.objects.in_site(current_site).filter(slug=slug)

    # If no page is found, fall back to searching the whole tree.
    if pages is None:
        pages = Page.objects.filter(slug=slug)

    return pages

class AzureSearchException (Exception):
    pass

# Custom search results class

class AzureSearchResults (BaseSearchResults):
    supports_facets = False

    def __init__ (self, backend, query_compiler, prefetch_related=None, results=None):
        super ().__init__ (backend, query_compiler)
        if results is not None:
            self._results_cache = results

class AzureEmptySearchResults (AzureSearchResults):
 
    def __init__ (self):
        super ().__init__ (None, None, [])


class AzureSearchRebuilder:
    def __init__(self, index):
        self.index = index

    def start(self):
        return self.index

    def finish(self):
        return

class AzureIndex:
    """Class for indexing items into Azure Search

    Data formatting and Azure Blob code taken from:
    https://dev.azure.com/nhsuk/dct.sample-cms/_git/dct.wagtail-funnelback-indexer?path=%2Fwagtailfunnelbackcontentindexer%2Ftasks.py
    """

    def __init__(self, storage):
        self._storage = storage
        self.name = storage.index_name

    def is_indexable(self, item):
        try:
            return item.search_indexable()
        except AttributeError:
            logger.info(f"'search_indexable' is not defined in {item}")
    
    def add_model (self, model):
        pass

    def refresh (self):
        pass

    def add_item(self, item):
        try:
            if self.is_indexable(item) and item.live:
                self.add_az_index_item(item)
            else:
                self._delete_from_azure_search(item)
                self._storage.delete_resource(item)
        except AttributeError as e: 
            logger.warning(f"Attribute not defined in {item}: {e}")

    def add_items(self, model, items):
        for item in items:
            self.add_item (item)

    def delete_item(self, item):
        try:
            if self.is_indexable(item):
                self._delete_from_azure_search(item)
                self._storage.delete_resource(item)
            else:
                return True
        except AttributeError: 
            logger.warning(f"page dict attribute is not defined in {item}")

    def _delete_from_azure_search(self, item):
        try:
            if self.is_indexable(item):
                azure_search = AzureSearchBackend({})
                azure_search.delete_search(item)
        except AttributeError: 
            logger.warning(f"page dict attribute is not defined in {item}")

    def add_taxonomy_terms(self, taxonomy_id, data):
        data = self._format_taxonomy_for_storage(data)
        self._storage.add_taxonomy_terms(taxonomy_id, data)

    def get_taxonomy_terms(self, taxonomy_id):
        data = self._storage.get_taxonomy_terms(taxonomy_id)
        if not data:
            logger.info(f"Taxonomies cache miss: {taxonomy_id}")
            try:
                terms = TaxonomyTerms.objects.get(taxonomy_id=taxonomy_id)
            except TaxonomyTerms.DoesNotExist:
                logger.error(f"Taxonomy terms for: {taxonomy_id} not found")
                return None
            data = self._format_taxonomy_for_storage(
                json.loads(terms.terms_json)
            )
            self._storage.add_taxonomy_terms(taxonomy_id, data)
        return data

    def add_az_index_item(self, page):
        if page.live:
            taxonomy_lookup = self.get_taxonomy_terms(page.TAXONOMY_TERMS_ID)
            if not taxonomy_lookup:
                logger.error(
                    "Cannot get taxonomy terms, skipping index item creation"
                )
                return

            # Build index json for a Resource item.
            index = {
                "resource": page.get_az_item()
            }

            # Reformat taxonomy terms for azure search.
            page_terms = json.loads(page.taxonomy_json or "{}")
            taxonomy_dict = self._taxonomy_dict_from_page_terms(
                page_terms, taxonomy_lookup["terms"]
            )
            for field in taxonomy_dict:
                index["resource"][field] = taxonomy_dict[field]

            self._storage.add_resource(page.id, index)
            logging.info ("Resource %s indexed", page.id)
            # No code presently to add via the live API if AZURE_SEARCH_UPDATE,
            # indexing occurs when/if an indexer crawls the container

    def _format_taxonomy_for_storage(self, taxonomy_data):
        terms_with_vocab = get_terms_from_terms_json(taxonomy_data)
        vocabs = get_vocabs_from_terms_json(taxonomy_data)
        content = {}
        content["vocabs"] = vocabs
        content["terms"] = terms_with_vocab
        return content

    def _taxonomy_dict_from_page_terms(self, page_terms, taxonomy_terms):
        page_term_groups = {}

        for page_term in page_terms:
            code = page_term["code"]

            try:
                taxonomy_term = taxonomy_terms[code]
                taxonomy_term_vocab_code = taxonomy_term["vocabCode"]
                taxonomy_term_index_path = taxonomy_term["indexPath"]

                taxonomy_key = "%s" % (taxonomy_term_vocab_code)

                if taxonomy_key in page_term_groups:
                    page_term_groups[taxonomy_key].append(
                        taxonomy_term_index_path
                    )
                else:
                    page_term_groups[taxonomy_key] = [taxonomy_term_index_path]

                # If it is a multi level taxonomy term then also
                # ensure the parent terms have been added
                if "|" in taxonomy_term_index_path:
                    parent_terms = self._get_parent_terms_from_index_path(
                        taxonomy_term_index_path
                    )
                    page_term_groups[taxonomy_key].extend(
                        parent_term
                        for parent_term in parent_terms
                        if parent_term not in page_term_groups[taxonomy_key]
                    )
            except Exception as e:
                logger.error("Unable to index page term %s: %s", code, e)

        d = {}
        for page_term_code in page_term_groups:
            terms = page_term_groups[page_term_code]
            d[page_term_code] = []
            for term in terms:
                d[page_term_code].append(term)

        return d

    def _get_parent_terms_from_index_path(self, taxonomy_term_index_path):
        """Extract the parents terms from an terms index path
        For example 'PARENTS|PARENTS3TO11|PARENTS3TO6|PARENTS3'
        Will return: [
        'PARENTS','PARENTS|PARENTS3TO11','PARENTS|PARENTS3TO11|PARENTS3TO6'
        ]
        """
        parent_terms = []
        while "|" in taxonomy_term_index_path:
            taxonomy_term_index_path, _term = taxonomy_term_index_path.rsplit(
                "|", 1
            )
            parent_terms.append(taxonomy_term_index_path)
        return parent_terms


class AzureSearchBackend(BaseSearchBackend):
    index_class = AzureIndex
    results_class = AzureSearchResults
    rebuilder_class = AzureSearchRebuilder

    def get_index_for_model(self, model):
        # use the cache storage until Azure Blob storage is set up, then use
        # `AzureStorage` when completed.

        if hasattr (settings, "AZURE_SEARCH_CONTAINER"):
            storage = AzureStorage()
        else:
            storage = CacheStorage()
        return AzureIndex(storage)

    """
    Parameters:
        sarch_value: example: "Search Value"
        fields_queryset: example: {"field": "lt value"}
        facets_queryset: example: {"TARGAUD": ["PARENTS"]}
        sort_by: example: "active_from_time desc"

    Sample url parameers:
        query: Better
        sort: title
        f.content/resource/TARGAUD: PARENTS
        f.content/resource/TARGAUD: PARENTS|PARENTS0TO2
        f.content/resource/TOPIC: WEANING

    Accepted
    """

    def azure_search(self, search_value, fields_queryset, facets_queryset, sort_by,results_per_page):
        url = self._create_azure_search_url_and_query(
            search_value, fields_queryset, facets_queryset, sort_by, results_per_page
        )
        headers = {"Subscription-Key": settings.AZURE_SEARCH["API_KEY"]}
        try:
            response = requests.get(url, headers=headers)
            json_response = {
                "search_content": json.loads(response.content),
                "ok": response.ok,
                "code": response.status_code,
            }
        except Exception as err:
            logger.error("Exception raised - Azure Search Get: %s", err)
            json_response = {
                "search_content": [],
                "ok": "failed",
                "code": 500,
            }
        return json_response
    
    # Implement Wagtail base query class method for use in Wagtail CMS searches
    def search(
        self,
        query,
        model_or_queryset,
        fields=None,
        operator=None,
        order_by_relevance=True,
        partial_match=False, # Partial matching in search is deprecated
    ):
        if not isinstance (query, PlainText):
            logger.error ("Only plain text queries are supported")
            # Would be nice if there were a SearchFeatureNotImplementedException,
            # but there doesn't seem to be one, a bit drastic to error the page as a generic 500
            # so return an unexplained empty result instead.
            return EmptySearchResults ()
        model = model_or_queryset.model if isinstance (model_or_queryset, QuerySet) else model_or_queryset
        if not (issubclass (model, PageQuerySet) or issubclass (model, Page)):
            logger.error ("Only page searches are supported, not model '%s'", model)
            return EmptySearchResults ()
        json_result = self.azure_search (
            query.query_string, {}, {}, None
        )
        ok = json_result.get ("ok")
        if ok:
            try:
                results = json_result ["search_content"] ["value"]
                result_urls = [
                    r ["content"] ["resource"] ["object_url"]
                    for r in results
                ]
            except Exception as e:
                logger.error ("Couldn't interpret search result: %s", e)
                raise

            pages = Page.objects.none ()
            for r in result_urls:
                page_slugs = ["home"] + [slug for slug in r.split ("/") if slug]
                pageOrPages = slugpages (page_slugs [-1])
                n = pageOrPages.count ()
                if n == 0:
                    logger.error ("Index entry for non-existent page %s", page_slugs [-1])
                else:
                    if n > 1:
                        logger.error ("%d pages share slug '%s'", n, page_slugs [-1])
                    pages = pages.union (pageOrPages)
            return AzureSearchResults (self, None, None, pages)

        else:
            code = json_result.get ("code")
            raise AzureSearchException (f"Azure search query failed, return code {code}")

    def delete_search(self, resource):
        fields_queryset = {"object_url": resource.url}
        response = self.azure_search("", fields_queryset, {}, "title asc")
        search_resource = None
        if response.get("code") == 200 and response['search_content']:
            if response['search_content']['value']:
                resources = response['search_content']['value']
                if len(resources) == 1:
                    search_resource = resources[0]
                else:
                    logger.info("Resource not found: {}".format(resource.id))
        else:
            logger.error("Invalid response: {}".format(response.get('search_content')))
        if search_resource:
            query_string = "api-version={}".format(
                settings.AZURE_SEARCH["DELETE_API_VERSION"]
            )
            url = "{}?{}".format(
                settings.AZURE_SEARCH["DELETE_API_HOST"],
                query_string
            )
            metadata_storage_path = search_resource.get(
                'metadata_storage_path'
            )
            delete_json = json.dumps({
                "value": [
                    {
                        "@search.action": "delete",
                        "metadata_storage_path": metadata_storage_path
                    }
                ]
            })
            headers = {
                "Subscription-Key": settings.AZURE_SEARCH["API_KEY"],
                "Content-Type": "application/json",
            }
            if settings.AZURE_SEARCH_UPDATE:
                try:
                    response = requests.post(url, headers=headers, data=delete_json)
                    if response.ok:
                        logger.info(
                            "Search resource deleted successfully for: {}".format(resource.id)
                        )
                    else:
                        logger.info(
                            "Error deleting the search resource: {} -- {}".format(
                                resource.id,
                                response.content
                            )
                        )
                except Exception as err:
                    logger.error("Exception raised - Azure Search Delete: %s", err)
            else:
                logger.info ("Search resource deletion noted for {} using {}".format(resource.id, url))

    def _create_azure_search_url_and_query(
        self, search_value, fields_queryset, facets_queryset, sort_by,results_per_page
    ):
        query_string = "search={}&api-version={}&searchMode=all".format(
            search_value, settings.AZURE_SEARCH["API_VERSION"]
        )
        filters = self._get_filters_from_fields(fields_queryset)
        filters = filters + self._get_filters_from_facets(facets_queryset)
        filters_query_string = self._build_query_string_from_filters(filters)
        sort_query_string = ""
        if sort_by:
            sort_query_string = "&$orderby={}{}".format(
                settings.AZURE_SEARCH["PREFIX"], sort_by
            )
        top = "&$top=" + results_per_page
        query_string = query_string + filters_query_string + sort_query_string + top
        return "{}?{}".format(settings.AZURE_SEARCH["API_HOST"], query_string)

    def _get_filters_from_fields(self, fields_queryset):
        filters = []
        for key, value in fields_queryset.items():
            filters.append(
                "({}{} eq '{}')".format(
                    settings.AZURE_SEARCH["PREFIX"], key, value
                )
            )
        return filters

    def _get_filters_from_facets(self, facets_queryset):
        filters = []
        for facet in facets_queryset.keys():
            val = facets_queryset[facet]

            facet_filters = val if type(val) == list else [val]
            for facet_filter in facet_filters:
                filters.append(
                    "({}{}/any(t: t eq '{}'))".format(
                        settings.AZURE_SEARCH["PREFIX"], facet, facet_filter
                    )
                )

        return filters

    def _build_query_string_from_filters(self, filters):
        filter_string = ""
        if len(filters) > 0:
            filter_string = "&$filter=("
            for value in filters:
                filter_string += "{} and ".format(value)
            filter_string = re.sub(" and $", "", filter_string)
            filter_string += ")"
        return filter_string

    def _build_query_sting_from_facet_categories(self, facets_filters):
        facet_categories = settings.AZURE_SEARCH["FACETS"] or ""
        facet_categories = facet_categories.split(",")

        query = ""
        for facet in facet_categories:
            query += "&facet={}{},count:100".format(
                settings.AZURE_SEARCH["PREFIX"], facet
            )

        return query


class DatabaseAzureSearchBackend(AzureSearchBackend):
    pass

SearchBackend = DatabaseAzureSearchBackend
