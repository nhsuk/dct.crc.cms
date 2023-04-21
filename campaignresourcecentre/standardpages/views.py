from io import StringIO
import sys

from logging import getLogger

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.cache import never_cache
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods

from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.notifications.dataclasses import ContactUsData
from campaignresourcecentre.notifications.adapters import gov_notify_factory

from .forms import ContactUsForm

logger = getLogger(__name__)


@require_http_methods(["GET"])
def cookie_declaration(request):
    return render(request, "cookies.html")


@require_http_methods(["GET"])
def cookie_settings(request):
    return render(request, "cookie_settings.html")


@require_http_methods(["GET"])
def cookie_confirmation(request):
    return render(request, "cookie_confirmation.html")


@require_http_methods(["POST", "GET"])
def contact_us(request):
    contact_us_form = ContactUsForm()
    if request.method == "POST":
        contact_us_form = ContactUsForm(request.POST)
        campaign = contact_us_form.data.get("healthy_behaviour")
        if campaign == "other":
            campaign = contact_us_form.data.get("other_campaign")
            contact_us_form.fields.get("other_campaign").required = True

        job_title = contact_us_form.data.get("job_title")
        if job_title == "student":
            contact_us_form.fields.get("organisation").required = False

        # Check the hidden form field has not been filled in by a spammer.
        if contact_us_form.data.get("cat6a"):
            logger.info("Spam detection field completed.")
        else:
            if contact_us_form.is_valid():
                payload = contact_us_form.data
                contact_us_data = ContactUsData(
                    payload.get("email"),
                    payload.get("first_name"),
                    payload.get("last_name"),
                    payload.get("job_title"),
                    payload.get("organisation"),
                    payload.get("organisation_type"),
                    campaign,
                    payload.get("audience"),
                    payload.get("engage_audience"),
                    payload.get("product_service"),
                    payload.get("message"),
                )

                gov_notify_factory().contact_submission(
                    settings.PHE_PARTNERSHIPS_EMAIL,
                    f"[CRC Contact Request] {campaign}",
                    contact_us_data,
                )
                return render(request, "thank_you_page.html")
    return render(request, "contact-us.html", {"form": contact_us_form})


@require_http_methods(["GET"])
def thank_you(request):
    return render(request, "thank_you_page.html")


@require_http_methods(["GET"])
def clear_cache(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cache.clear()
    return HttpResponse("Cache has been cleared")


@require_http_methods(["GET"])
def update_index(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    with StringIO() as responseFile:
        call_command("update_index", stdout=responseFile, stderr=responseFile)
        responseFile.seek(0)
        response = HttpResponse(responseFile.read())
        response.headers["Content-Type"] = "text/plain"
        return response


@require_http_methods(["GET"])
def search_orphans(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    with StringIO() as responseFile:
        call_command("searchorphans", stdout=responseFile, stderr=responseFile)
        responseFile.seek(0)
        response = HttpResponse(responseFile.read())
        response.headers["Content-Type"] = "text/plain"
        return response


@require_http_methods(["GET"])
def session_summary(request):
    # Abbreviated to avoid the overhead of running all the context processors
    session = request.session
    logged_in = "ParagonUser" in session
    basket = Basket(session)
    t = loader.get_template("molecules/header/account.html")
    return HttpResponse(
        t.render(
            {"logged_in": logged_in, "BASKET_ITEM_COUNT": basket.get_items_count()}
        )
    )
