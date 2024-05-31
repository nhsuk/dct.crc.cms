import json
import logging

from django.template.response import TemplateResponse
from django.shortcuts import render
from wagtailreacttaxonomy.models import TaxonomyTerms
from campaignresourcecentre.search.azure import AzureSearchBackend
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def _search(request):
    user_role = (
        request.session.get("UserDetails")
        and request.session.get("UserDetails")["ProductRegistrationVar1"]
    )
    query_string = request.GET
    taxonomy_json = json.loads(
        TaxonomyTerms.objects.get(taxonomy_id="crc_taxonomy").terms_json
    )
    parent_taxonomy_codes = [taxonomy.get("code") for taxonomy in taxonomy_json]
    search_query = query_string.get("q", "")
    sort = query_string.get("sort")
    results_per_page = "1000"
    search_results = []
    search_value = ""

    # Azure Search
    if search_query:
        search_value = search_query

    search = AzureSearchBackend({})
    fields_queryset = {"objecttype": "resource"}
    facets_queryset = {}
    for taxonomy_code in parent_taxonomy_codes:
        taxonomy_value = query_string.getlist(taxonomy_code)
        if len(taxonomy_value) > 0 and taxonomy_value[0] != "":
            facets_queryset[taxonomy_code] = taxonomy_value

    sort_by = None
    if sort == "oldest":
        sort_by = "last_published_at"
    elif sort == "newest" or search_query == "":
        sort_by = "last_published_at desc"

    response = search.azure_search(
        search_value, fields_queryset, facets_queryset, sort_by, results_per_page
    )

    resources = []
    if (
        response.get("search_content")
        and response["search_content"].get("value") != None
    ):
        resources = response["search_content"]["value"]
    elif response.get("search_content") and response["search_content"].get("Message"):
        logger.info(
            f"Azure Search Issue:{response.get('search_content').get('Message')}"
        )
    else:
        logger.info(
            f"Azure Search Issue: neither search content values nor message returned"
        )

    search_results = [
        {
            "title": resource["content"]["resource"].get("title"),
            "campaign_title": resource["content"]["resource"].get("campaign_title"),
            "campaign_url": resource["content"]["resource"].get("campaign_url"),
            "summary": resource["content"]["resource"].get("summary"),
            "image_url": resource["content"]["resource"].get("image_url"),
            "image_alt": resource["content"]["resource"].get("image_alt"),
            "listing_summary": resource["content"]["resource"].get("summary"),
            "url": resource["content"]["resource"].get("object_url"),
            "permission_role": resource["content"]["resource"].get("permission_role"),
        }
        for resource in resources
    ]

    response = {
        "search_query": search_query,
        "sort": sort,
        "search_results": search_results,
        "count": len(search_results),
        "taxonomies": taxonomy_json,
        "user_role": (user_role or "").lower(),
        "facets_queryset": facets_queryset,
    }
    return response


@require_http_methods(["GET"])
def search(request):
    search = _search(request)
    response = TemplateResponse(request, "search.html", search)
    return response


@require_http_methods(["GET"])
def render_search(request):
    search = _search(request)
    response = render(request, "molecules/search-result/refresh-search.html", search)
    return response
