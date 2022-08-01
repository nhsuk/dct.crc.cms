from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def format_date(date):
    try:
        date_time_obj = datetime.strptime(date, "%Y-%m-%d")
        return date_time_obj.strftime("%d/%m/%Y")
    except:  # noqa
        return date
