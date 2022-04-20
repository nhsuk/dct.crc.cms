from django import template

register = template.Library()


# This is used in templates to get dictionaries with a '-' in them.
@register.filter
def get(mapping, key):
    return mapping.get(key, "")
