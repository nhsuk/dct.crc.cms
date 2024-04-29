from django import template
from campaignresourcecentre.resources.models import ResourceItem
import logging

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def get_field(sku):
    # Find the first resource item, if any, matching this SKU
    resource_item = ResourceItem.objects.filter(sku=sku).first()
    if not resource_item:
        logger.error("No resource item with SKU '%s'" % sku)
        resource_item = ResourceItem()
        resource_item.title = "Item not found"
    return resource_item
