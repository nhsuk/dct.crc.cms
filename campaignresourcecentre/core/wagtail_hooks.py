from logging import getLogger

from django.conf import settings
from django.http import HttpResponseBadRequest
from wagtail.core import hooks

logger = getLogger(__name__)


@hooks.register("before_publish_page")
def remove_publication_rights_from_nhse_editors(request, page):
    if settings.RESTRICTED_PUBLISHING_GROUP_NAME:
        restricted = request.user.groups.filter(
            name=settings.RESTRICTED_PUBLISHING_GROUP_NAME
        )
        if restricted:
            logger.error("Publication denied to user")
            return HttpResponseBadRequest("You do not have permission to publish pages")
    logger.info("Page published by unrestricted user")
