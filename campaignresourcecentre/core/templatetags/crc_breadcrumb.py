import logging

from django import template
from wagtail.models import Page

logger = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag("wagtailnhsukfrontend/breadcrumb.html", takes_context=True)
def crc_breadcrumb(context):
    page = context.get("page", None)
    if isinstance(page, Page):
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
        return {"breadcrumb_pages": [home] + list(breadcrumb_pages)}
    else:
        logger.error("No current page found for breadcrumb")
        return {"breadcrumb_pages": []}
