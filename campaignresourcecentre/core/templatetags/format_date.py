import logging

from django import template
from datetime import datetime

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def format_date(date):
    try:
        date_time_obj = datetime.strptime(date, "%Y-%m-%d")
        return date_time_obj.strftime("%d/%m/%Y")
    except Exception as e:
        logger.error("Invalid date object '%s' (%s)", date, e)
        return str(date)
