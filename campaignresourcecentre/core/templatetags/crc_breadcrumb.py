from django import template
from wagtail.core.models import Page

register = template.Library()


@register.inclusion_tag("wagtailnhsukfrontend/breadcrumb.html", takes_context=True)
def crc_breadcrumb(context):

    page = context.get("page", None)
    if not isinstance(page, Page):
        raise Exception("'page' not found in template context")
    site = page.get_site()
    # Get pages which are an ancestor of the current page, but limited to pages under the site root (a.k.a the homepage)
    breadcrumb_pages = (
        page.get_ancestors(inclusive=False)
        .descendant_of(site.root_page, inclusive=False)
        .order_by("depth")
    )
    # Add the current page to the end with hardcoded title
    home = site.root_page
    home.title = "Home"

    return {
        "breadcrumb_pages": [home] + list(breadcrumb_pages),
    }
