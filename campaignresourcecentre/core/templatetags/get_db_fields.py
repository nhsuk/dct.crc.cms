from django import template
from campaignresourcecentre.resources.models import ResourceItem
import logging

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def get_field(sku):
    try:
        return ResourceItem.objects.get(sku=sku)
    except Exception as err:
        logger.info(err)
