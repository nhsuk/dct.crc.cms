import json
import re
import logging
import requests

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from django.conf import settings
from django.db.models.query import QuerySet

from wagtail.models import Page, PageQuerySet

from wagtailreacttaxonomy.models import (
    TaxonomyTerms,
    get_terms_from_terms_json,
    get_vocabs_from_terms_json,
)
from wagtail.search.backends.base import (
    BaseSearchBackend,
    BaseSearchResults,
    EmptySearchResults,
)
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


class AzureSearchException(Exception):
    pass


# Custom search results class


class AzureSearchResults(BaseSearchResults):
    supports_facets = False

    def __init__(self, backend, query_compiler, prefetch_related=None, results=None):
        super().__init__(backend, query_compiler)
        if results is not None:
            self._results_cache = results


class AzureEmptySearchResults(AzureSearchResults):
    def __init__(self):
        super().__init__(None, None, [])


class AzureSearchRebuilder:
    def __init__(self, index):
        logger.info("Initiating search rebuild for '%s' index", index)
        self.index = index

    def _extract_result_urls(self, json_result, result):
        search_content = json_result["search_content"]
        try:
            results = search_content.get("value")
        except Exception as e:
            logger.error("Can't get search results: %s", e)
            results = []
        for r in results:
            search_object = r["content"]["resource"]
            url = search_object["object_url"] if search_object else None
            if url:
                if url in result:
                    result[url].append(r)
                else:
                    result[url] = [r]

    def retrieve_current_search_objects(self):
        azure_search = AzureSearchBackend({})
        json_result = azure_search.azure_search("", {}, {}, None, 1000)
        ok = json_result.get("ok")
        result = {}
        if ok:
            try:
                self._extract_result_urls(json_result, result)
                logger.info(f"Current result URLs: {len (result)}")
            except Exception as e:
                logger.error("Couldn't interpret search result: %s", e)
                raise
        else:
            logger.error(f"Not OK result from retrieving search objects: {json_result}")
        return result

    def start(self):
        logger.info("Starting search rebuild")
        self.preexisting_objects = self.retrieve_current_search_objects()
        logger.info(
            "URLs of indexed objects at start: %d", len(self.preexisting_objects)
        )
        if self.preexisting_objects:
            # Delete them all
            azure_search = AzureSearchBackend({})
            for url, search_resources in self.preexisting_objects.items():
                for search_resource in search_resources:
                    azure_search.delete_search_resource(search_resource)
        return self.index

    def finish(self):
        logger.info("Completed search rebuild")
        storage = self.index._storage
        added_urls = set(i[1] for i in storage.added_items)
        added_items = sorted(list(storage.added_items), key=lambda x: x[1])
        deleted_items = sorted(list(storage.deleted_items))
        logger.info("%d search item(s) added", len(added_items))
        if len(added_items):
            logger.info("First added is %s, last %s", added_items[0], added_items[-1])
        logger.info("%d search item(s) deleted", len(deleted_items))
        if len(deleted_items):
            logger.info(
                "First deleted is %s, last %s", deleted_items[0], deleted_items[-1]
            )
        postexisting_objects = self.retrieve_current_search_objects()
        postexisting_urls = set(postexisting_objects.keys())
        urls = sorted(postexisting_urls)
        logger.info("%d search item(s) indexed after update", len(urls))
        if len(urls):
            logger.info("First indexed is %s, last is %s", urls[0], urls[-1])
        added_and_deleted_urls = added_urls & storage.deleted_items
        if added_and_deleted_urls:
            logger.error("Items added and deleted: %s", added_and_deleted_urls)
        indexed_and_deleted_urls = postexisting_urls & storage.deleted_items
        if indexed_and_deleted_urls:
            logger.error("Items indexed and deleted: %s", indexed_and_deleted_urls)
        indexed_and_not_added_urls = postexisting_urls - added_urls
        if indexed_and_not_added_urls:
            logger.error(
                "%d item(s) indexed but not added", len(indexed_and_not_added_urls)
            )
            self.index._storage.add_json_file(
                f"orphans_{self.index.name}.json",
                {url: postexisting_objects[url] for url in indexed_and_not_added_urls},
            )
            for i, url in enumerate(sorted(indexed_and_not_added_urls)):
                logger.error("Orphan index item %d: %s", i + 1, url)
                entries = len(postexisting_objects[url])
                if entries > 1:
                    logger.error("%s instances of url %s in index", entries, url)

        return


class AzureIndex:
    """Class for indexing items into Azure Search

    Data formatting and Azure Blob code taken from:
    https://dev.azure.com/nhsuk/dct.sample-cms/_git/dct.wagtail-funnelback-indexer?path=%2Fwagtailfunnelbackcontentindexer%2Ftasks.py
    """

    def __init__(self, storage):
        self._storage = storage
        self.name = storage.index_name
        logger.info("Initialising Azure index %s", self.name)

    def is_indexable(self, item):
        try:
            return item.search_indexable()
        except AttributeError:
            logger.info(f"'search_indexable' is not defined in {item}")
            return False

    def add_model(self, model):
        pass

    def refresh(self):
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
            self.add_item(item)

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
            data = self._format_taxonomy_for_storage(json.loads(terms.terms_json))
            self._storage.add_taxonomy_terms(taxonomy_id, data)
        return data

    def add_az_index_item(self, page):
        if page.live:
            taxonomy_lookup = self.get_taxonomy_terms(page.TAXONOMY_TERMS_ID)
            if not taxonomy_lookup:
                logger.error("Cannot get taxonomy terms, skipping index item creation")
                return

            # Build index json for a Resource item.
            index = {"resource": page.get_az_item()}
            index["resource"]["id"] = page.id

            # Reformat taxonomy terms for azure search.
            page_terms = json.loads(page.taxonomy_json or "{}")
            taxonomy_dict = self._taxonomy_dict_from_page_terms(
                page_terms, taxonomy_lookup["terms"]
            )
            for field in taxonomy_dict:
                index["resource"][field] = taxonomy_dict[field]

            self._storage.add_resource(page.id, index)
            logging.info("Resource %s indexed", page.id)
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
                    page_term_groups[taxonomy_key].append(taxonomy_term_index_path)
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
            taxonomy_term_index_path, _term = taxonomy_term_index_path.rsplit("|", 1)
            parent_terms.append(taxonomy_term_index_path)
        return parent_terms


class AzureSearchBackend(BaseSearchBackend):
    index_class = AzureIndex
    results_class = AzureSearchResults
    rebuilder_class = AzureSearchRebuilder

    def get_index_for_model(self, model):
        # use the cache storage until Azure Blob storage is set up, then use
        # `AzureStorage` when completed.

        if hasattr(settings, "AZURE_SEARCH_CONTAINER"):
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

    Sample url parameters:
        query: Better
        sort: title
        f.content/resource/TARGAUD: PARENTS
        f.content/resource/TARGAUD: PARENTS|PARENTS0TO2
        f.content/resource/TOPIC: WEANING

    Accepted
    """

    def azure_search(
        self,
        search_value,
        fields_queryset,
        facets_queryset,
        sort_by,
        results_per_page=None,
    ):
        url = self._create_azure_search_url_and_query(
            search_value, fields_queryset, facets_queryset, sort_by, results_per_page
        )
        logger.info("Searching for %s", url)
        headers = {"Subscription-Key": settings.AZURE_SEARCH["API_KEY"]}
        try:
            response = requests.get(url, headers=headers)
            if len(response.content) > 0:
                content = response.json()
            else:
                logger.warn(
                    f"Azure search returned '{response.status_code}' status code and no content in response, returning no matching results"
                )
                content = {"value": []}

            json_response = {
                "search_content": content,
                "ok": response.ok,
                "code": response.status_code,
            }
            not_interpretable = 0
            try:
                results = json_response["search_content"]["value"]
                result_urls = []
                for r in results:
                    content = r.get("content")
                    resource = content.get("resource") if content else None
                    object_url = resource.get("object_url") if resource else None
                    if object_url:
                        result_urls.append(object_url)
                    else:
                        not_interpretable += 1
                        logger.error("--Can't interpret result: %s", r)
            except Exception as e:
                logger.error("Couldn't interpret search response: %s", e)
                raise

            logger.info(
                "%d items returned from search%s",
                len(result_urls),
                (
                    f", {not_interpretable} not interpretable"
                    if not_interpretable > 0
                    else ""
                ),
            )
        except Exception as err:
            logger.error("Exception raised - Azure Search Get: %s", err)
            json_response = {"ok": False, "code": 500}

        return json_response

    # Implement Wagtail base query class method for use in Wagtail CMS searches
    def search(
        self,
        query,
        model_or_queryset,
        fields=None,
        operator=None,
        order_by_relevance=True,
        partial_match=False,  # Partial matching in search is deprecated
    ):
        logger.info("Searching for %s", query)
        if isinstance(query, str):
            query_string = query
        elif not isinstance(query, PlainText):
            query_string = query.query_string
        else:
            logger.error("Only plain text queries are supported")
            # Would be nice if there were a SearchFeatureNotImplementedException,
            # but there doesn't seem to be one, a bit drastic to error the page as a generic 500
            # so return an unexplained empty result instead.
            return EmptySearchResults()
        model = (
            model_or_queryset.model
            if isinstance(model_or_queryset, QuerySet)
            else model_or_queryset
        )
        if not (issubclass(model, PageQuerySet) or issubclass(model, Page)):
            logger.error("Only page searches are supported, not model '%s'", model)
            return EmptySearchResults()
        json_result = self.azure_search(query_string, {}, {}, None)
        ok = json_result.get("ok")
        if ok:
            try:
                results = json_result["search_content"]["value"]
                result_urls = [r["content"]["resource"]["object_url"] for r in results]
            except Exception as e:
                logger.error("Couldn't interpret CMS search result: %s", e)
                raise
            logger.info("%d items returned from search", len(result_urls))
            pages = Page.objects.none()
            for r in result_urls:
                page_slugs = ["home"] + [slug for slug in r.split("/") if slug]
                page_or_pages = slugpages(page_slugs[-1])
                n = page_or_pages.count()
                if n == 0:
                    logger.error("Index entry for non-existent page %s", page_slugs[-1])
                else:
                    if n > 1:
                        logger.error("%d pages share slug '%s'", n, page_slugs[-1])
                    pages = pages.union(page_or_pages)
            return AzureSearchResults(self, None, None, pages)

        else:
            code = json_result.get("code")
            raise AzureSearchException(f"Azure search query failed, return code {code}")

    def delete_search(self, resource):
        fields_queryset = {"object_url": resource.url}
        response = self.azure_search("", fields_queryset, {}, "title asc")
        if response.get("code") == 200 and response["search_content"]:
            if response["search_content"]["value"]:
                resources = response["search_content"]["value"]
                if len(resources) == 1:
                    self.delete_search_resource(resources[0])
                else:
                    logger.info(
                        "Resource to delete not found or ambiguous - {}".format(
                            resources
                        )
                    )
        else:
            logger.error("Invalid response: {}".format(response.get("search_content")))

    def delete_search_resource(self, search_resource):
        try:
            resource_url = search_resource["content"]["resource"]["object_url"]
        except KeyError:
            resource_url = "unknown URL"
        query_string = "api-version={}".format(
            settings.AZURE_SEARCH["DELETE_API_VERSION"]
        )
        url = "{}?{}".format(settings.AZURE_SEARCH["DELETE_API_HOST"], query_string)
        metadata_storage_path = search_resource.get("metadata_storage_path")
        delete_json = json.dumps(
            {
                "value": [
                    {
                        "@search.action": "delete",
                        "metadata_storage_path": metadata_storage_path,
                    }
                ]
            }
        )
        headers = {
            "Subscription-Key": settings.AZURE_SEARCH["API_KEY"],
            "Content-Type": "application/json",
        }
        if settings.AZURE_SEARCH_UPDATE:
            try:
                response = requests.post(url, headers=headers, data=delete_json)
                if response.ok:
                    logger.info(
                        "Search resource deleted successfully for: {}".format(
                            resource_url
                        )
                    )
                else:
                    logger.info(
                        "Error deleting the search resource {} using {}: {}".format(
                            resource_url, url, response.content
                        )
                    )
            except Exception as err:
                logger.error(
                    "Exception raised using %s - Azure Search Delete: %s", url, err
                )
        else:
            logger.info(
                "Search resource deletion noted for {} using {}".format(
                    resource_url, url
                )
            )

    def _create_azure_search_url_and_query(
        self, search_value, fields_queryset, facets_queryset, sort_by, results_per_page
    ):
        query_string = "search={}&api-version={}&searchMode=all".format(
            escape(requests.utils.quote(search_value)),
            settings.AZURE_SEARCH["API_VERSION"],
        )
        filters = self._get_filters_from_fields(fields_queryset)
        filters = filters + self._get_filters_from_facets(facets_queryset)
        filters_query_string = self._build_query_string_from_filters(filters)
        sort_query_string = ""
        if sort_by:
            sort_query_string = "&$orderby={}{}".format(
                settings.AZURE_SEARCH["PREFIX"], sort_by
            )
        top = "" if results_per_page is None else "&$top=" + str(results_per_page)
        query_string = query_string + filters_query_string + sort_query_string + top

        return "{}?{}".format(settings.AZURE_SEARCH["API_HOST"], query_string)

    def _get_filters_from_fields(self, fields_queryset):
        filters = []
        for key, value in fields_queryset.items():
            filters.append(
                "({}{} eq '{}')".format(settings.AZURE_SEARCH["PREFIX"], key, value)
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
            filter_string = "("
            for value in filters:
                filter_string += "{} and ".format(value)
            filter_string = re.sub(" and $", "", filter_string)
            filter_string += ")"
            filter_string = "&$filter=" + requests.utils.quote(filter_string)
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
