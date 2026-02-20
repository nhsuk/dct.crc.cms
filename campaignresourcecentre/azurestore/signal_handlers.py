import json

from django.dispatch import receiver
from django.db.models.signals import post_save

from campaignresourcecentre.search.azure import AzureIndex
from campaignresourcecentre.wagtailreacttaxonomy.models import (
    TaxonomyTerms,
    load_campaign_topics,
)

from .utils import CacheStorage


@receiver(post_save, sender=TaxonomyTerms)
def update_taxonomy_terms_in_cache(sender, instance, **kwargs):
    """Save the taxonomy data to the cache. Use during development when Azure
    Blob Store isn't configured"""
    data = json.loads(instance.terms_json)
    load_campaign_topics(data)
    index = AzureIndex(CacheStorage())
    index.add_taxonomy_terms(instance.taxonomy_id, data)
