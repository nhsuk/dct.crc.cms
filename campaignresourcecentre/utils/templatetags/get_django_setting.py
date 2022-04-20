from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_django_setting(setting_name):
    """Get a value out of the django settings, or an empty string if it doesn't exist."""

    return getattr(settings, setting_name, "")