from django import template


register = template.Library()


@register.filter
def taxonomies_get(h, key):
    return h.get(key)


@register.filter
def code_includes(codes, code):
    return code in codes


@register.filter
def length(dict):
    return len(dict)


@register.filter
def filters_added(dict):
    return len(dict) > 3 or (
        len(dict) > 0 and (dict.get('TOPIC') != [''] or
                           dict.get('REGION') != [''] or
                           dict.get('LANGUAGE') != [''])
    )
