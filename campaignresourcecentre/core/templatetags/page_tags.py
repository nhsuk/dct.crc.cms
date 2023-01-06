from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_parent(context):
    page = context.get("page", None)
    parent = page.get_parent(update=True) if page else None
    return parent or "Campaign Resource Centre"
