from django.core.management import call_command
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(["GET"])
def publish_pages(request):
    """Publish pages that are scheduled to be published"""

    pubToken = getattr(settings, "PUBTOKEN", None)

    if request.is_secure() and request.META.get("pubToken", "") == pubToken:
        call_command("publish_scheduled_pages")
        return HttpResponse("ok", status=202)

    # return 401 django error page
    return HttpResponse(status=401)
