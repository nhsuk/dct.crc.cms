import logging
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from campaignresourcecentre.core.helpers import verify_pubtoken

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def publish_pages(request):
    """Publish pages that are scheduled to be published and unpublish pages that are scheduled to expire"""
    try:
        if verify_pubtoken(request):
            logger.info("Start: management command 'publish_scheduled'")
            call_command("publish_scheduled")
            logger.info("End: management command 'publish_scheduled'")
            return HttpResponse(
                "Published scheduled pages and unpublished expired pages", status=202
            )
    except TypeError:
        logger.warning("PUBTOKEN not set")
        raise PermissionDenied
    # return 401 django error page
    logger.warning("Unauthorized publish_pages request")
    raise PermissionDenied
