from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_parent(context):
    page = context.get("page", None)
    parent = page.get_parent(update=True)
    return parent or "Campaign Resource Centre"
