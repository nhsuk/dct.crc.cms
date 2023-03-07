import logging
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from wagtail.core.models import PageRevision

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def publish_pages(request):
    """Publish pages that are scheduled to be published"""

    pubtoken = getattr(settings, "PUBTOKEN", None)
    try:
        if request.headers.get("Authorization", "") == "Bearer " + pubtoken:
            future_pages = len(
                PageRevision.objects.filter(approved_go_live_at__lt=timezone.now())
            )
            if future_pages > 0:
                logger.info("publishing " + str(future_pages) + " scheduled pages")
                call_command("publish_scheduled_pages")
            else:
                logger.info("No scehduled pages")
            return HttpResponse("ok", status=202)
    except TypeError:
        logger.warning("PUBTOKEN not set")
        raise PermissionDenied
    # return 401 django error page
    logger.warning("Unauthorized publish_pages request")
    raise PermissionDenied
