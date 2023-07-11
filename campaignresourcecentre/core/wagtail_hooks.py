from logging import getLogger

from django.conf import settings
from django.http import HttpResponseBadRequest
from wagtail import hooks

logger = getLogger(__name__)

from django.utils.html import format_html
from django.templatetags.static import static


@hooks.register("insert_global_admin_css")
def insert_global_admin_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}">',
        static("admin/css/admin.css"),
    )
