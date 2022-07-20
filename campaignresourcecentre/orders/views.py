from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render

# Beware this exception is specific to Postgres. It presents as a Postgres error, not an integrity error
from psycopg2.errors import UniqueViolation

import datetime
import logging

from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError

from .forms import DeliveryAddressForm

from .models import OrderSequenceNumber

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def summary(request):
    basket = Basket(request.session)
    items = basket.get_all_items().items()
    delivery_address = request.session.get("DELIVERY_ADDRESS")
    delivery_address = {
        "Full name": delivery_address.get("Address1"),
        "Address line 1": delivery_address.get("Address2"),
        "Address line 2": delivery_address.get("Address3"),
        "City or town": delivery_address.get("Address4"),
        "Postcode": delivery_address.get("Address5"),
    }
    if not delivery_address:
        return redirect("/orders/address/edit")
    return render(
        request, "summary.html", {"items": items, "delivery_address": delivery_address}
    )


@require_http_methods(["GET", "POST"])
def delivery_address(request):
    user_token = request.session.get("ParagonUser")
    if request.method == "POST":
        f = DeliveryAddressForm(request.POST)
        paragon_client = Client()
        if f.is_valid():
            request.session["DELIVERY_ADDRESS"] = f.cleaned_data
            response = paragon_client.set_user_address(user_token, f.cleaned_data)
            if response["code"] == 200:
                return redirect("/orders/summary")
    else:
        delivery_address = request.session.get("DELIVERY_ADDRESS")
        f = DeliveryAddressForm(delivery_address)
    return render(request, "delivery_address.html", {"form": f})


@require_http_methods(["POST"])
def place_order(request):
    try:
        with transaction.atomic():
            try:
                osn = OrderSequenceNumber.objects.get(date=datetime.date.today())
                osn.seq_number = osn.seq_number + 1
                osn.save()
            except OrderSequenceNumber.DoesNotExist:
                try:
                    osn = OrderSequenceNumber()
                    osn.date = datetime.date.today()
                    osn.seq_number = 1
                    osn.save()
                    logger.info("First order of %s", osn.date)
                except UniqueViolation:
                    logger.info("Concurrent initial orders on %s - retrying", osn.date)
                    osn = OrderSequenceNumber.objects.get(date=datetime.date.today())
                    osn.seq_number = osn.seq_number + 1
                    osn.save()
            order_number = osn.order_number
            basket = Basket(request.session)
            items = basket.get_all_items().values()
            user_token = request.session.get("ParagonUser")
            paragon_client = Client()
            try:
                response = paragon_client.create_order(user_token, order_number, items)
                if response["status"] == "ok":
                    basket.empty_basket()
                    return render(
                        request, "thank_you.html", {"order_number": order_number}
                    )
            except ParagonClientError as PCE:
                for error in PCE.args:
                    logger.error("Paragon ClientError: " + error)
                raise
    except ParagonClientError:
        return redirect("/orders/summary")


def get_address_from_paragon(user_token):
    paragon_client = Client()
    delivery_address = paragon_client.get_user_address(user_token)
    delivery_address = delivery_address["content"]
    delivery_address.pop("ProductToken")
    delivery_address.pop("UserToken")
    return delivery_address
