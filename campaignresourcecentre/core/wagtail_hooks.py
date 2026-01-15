from logging import getLogger

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.utils.html import format_html
from django.templatetags.static import static
from wagtail import hooks

from campaignresourcecentre.core.tag_management.bulk_actions import ManageTagsBulkAction

logger = getLogger(__name__)


@hooks.register("insert_global_admin_css")
def insert_global_admin_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}">',
        static("admin/css/admin.css"),
    )


@hooks.register("register_bulk_action")
class RegisterManageTagsBulkAction(ManageTagsBulkAction):
    pass
