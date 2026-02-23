from django import template
import json
import logging

from campaignresourcecentre.wagtailreacttaxonomy.models import (
    TaxonomyTerms,
    load_campaign_topics,
)

register = template.Library()
logger = logging.getLogger(__name__)

# Store the full taxonomy to be used as a lookup table.
try:
    data = json.loads(TaxonomyTerms.objects.get(taxonomy_id="crc_taxonomy").terms_json)
    load_campaign_topics(data)
except Exception as e:  # noqa
    logger.info("Error loading taxonomy JSON (%s)", e)
    data = {}


# Find the parent label of the JSON object
def get_label(arg):
    for item in data:
        for subitm in item["children"]:
            if subitm["code"] == arg:
                return item["code"]


@register.simple_tag
def get_taxonomies(taxonomy, category):
    results = []
    for item in taxonomy:
        for key, value in item.items():
            if key == "code" and get_label(value) == category:
                results.append(item["label"])
    return ", ".join(results)
