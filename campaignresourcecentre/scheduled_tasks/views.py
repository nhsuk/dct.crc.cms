import logging
from django.apps import apps
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from wagtail.models import DraftStateMixin, Page, Revision

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def publish_pages(request):
    """Publish pages that are scheduled to be published and unpublish pages that are scheduled to expire
    This method is based on and utilises wagtail's 'publish_scheduled' command:
    https://github.com/wagtail/wagtail/blob/9084c196fad5db29aeae9f9c6ab9eca06dd9bd14/wagtail/management/commands/publish_scheduled.py
    """

    pubtoken = "token"  # getattr(settings, "PUBTOKEN", None)
    try:
        if request.headers.get("Authorization", "") == "Bearer " + pubtoken:
            pages_to_publish = get_pages_to_publish()
            pages_to_unpublish = get_pages_to_unpublish()
            if len(pages_to_publish) > 0 or len(pages_to_unpublish) > 0:
                response = f"Publishing {len(pages_to_publish)} scheduled page(s) and unpublishing {len(pages_to_unpublish)} expired page(s)"
                call_command("publish_scheduled")
            else:
                response = "No scehduled page actions"

            logger.info(response)
            return HttpResponse(response, status=202)
    except TypeError:
        logger.warning("PUBTOKEN not set")
        raise PermissionDenied
    # return 401 django error page
    logger.warning("Unauthorized publish_pages request")
    raise PermissionDenied


def get_pages_to_publish():
    return Revision.objects.filter(approved_go_live_at__lt=timezone.now())


def get_pages_to_unpublish():
    models = [Page]
    models += [
        model
        for model in apps.get_models()
        if issubclass(model, DraftStateMixin) and not issubclass(model, Page)
    ]

    expired_objects = []
    for model in models:
        expired = model.objects.filter(live=True, expire_at__lt=timezone.now())
        expired_objects += expired

    return expired_objects
