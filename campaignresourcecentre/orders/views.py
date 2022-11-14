from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

# Beware this exception is specific to Postgres. It presents as a Postgres error, not an integrity error
from psycopg2.errors import UniqueViolation

import datetime
import logging
import json
from django.utils import timezone

from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError
from campaignresourcecentre.paragon_users.decorators import paragon_user_logged_in
from campaignresourcecentre.utils.views import bad_request
from campaignresourcecentre.paragon_users.helpers.postcodes import get_postcode_data
from campaignresourcecentre.paragon.helpers.reporting import send_report

from .forms import DeliveryAddressForm

from .models import OrderSequenceNumber

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
@paragon_user_logged_in
def summary(request):
    basket = Basket(request.session)
    items = basket.get_all_items().items()
    delivery_address = request.session.get("DELIVERY_ADDRESS")
    if not delivery_address:
        return redirect("/orders/address/edit")
    delivery_address = {
        "Full name": delivery_address.get("Address1"),
        "Address line 1": delivery_address.get("Address2"),
        "Address line 2": delivery_address.get("Address3"),
        "City or town": delivery_address.get("Address4"),
        "Postcode": delivery_address.get("Address5"),
    }

    # items_in_basket permits disabling place order if that page
    # is ever presented with an empty basket
    return render(
        request,
        "summary.html",
        {
            "items": items,
            "delivery_address": delivery_address,
            "items_in_basket": len(items),
        },
    )


@require_http_methods(["GET", "POST"])
@paragon_user_logged_in
def delivery_address(request):
    user_token = request.session.get("ParagonUser")
    if request.method == "POST":
        f = DeliveryAddressForm(request.POST)
        paragon_client = Client()
        if f.is_valid():
            request.session["DELIVERY_ADDRESS"] = f.cleaned_data
            try:
                response = paragon_client.set_user_address(user_token, f.cleaned_data)
                return redirect("/orders/summary")
            # This doesn't seem to be called whatever is given as address to Parkhouse
            # so it should be treated as an unknown problem, i.e. server error
            except ParagonClientError as PCE:
                for error in PCE.args:
                    logger.error("Paragon ClientError: " + error)
                raise
        # if not valid, fall through and represent the form
    else:
        delivery_address = request.session.get("DELIVERY_ADDRESS")
        f = DeliveryAddressForm(delivery_address)
    return render(request, "delivery_address.html", {"form": f})


@require_http_methods(["POST"])
@paragon_user_logged_in
def place_order(request):
    user_token = request.session.get("ParagonUser")
    paragon_client = Client()
    basket = Basket(request.session)
    items = basket.get_all_items().values()
    address = delivery_address = request.session.get("DELIVERY_ADDRESS")

    # Front-end shouldn't ever route to this entry with an empty basket
    if len(items) == 0:
        return bad_request(request, "Incomplete address")
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
        try:
            response = paragon_client.create_order(user_token, order_number, items)
            if response["status"] == "ok":
                basket.empty_basket()

                # send off data to reporting
                date = timezone.now().strftime("%Y-%m-%d")
                postcode = delivery_address.get("Address5")
                postcode_data = get_postcode_data(postcode)
                checkout_items = []

                for item in items:
                    checkout_item = {
                        "itemCode": item.get("item_code"),
                        "quantity": item.get("quantity"),
                        "url": item.get("url"),
                        "campaign": item.get("campaign"),
                        "imageUrl": item.get("image_url"),
                        "title": item.get("title"),
                    }
                    checkout_items.append(checkout_item)

                data_dump = json.dumps(
                    {
                        "userToken": user_token,
                        "postcode": postcode,
                        "crcOrderNumber": order_number,
                        "orderItems": checkout_item,
                        "orderDate": date,
                        "longitude": postcode_data.get("longitude"),
                        "latitude": postcode_data.get("latitude"),
                        "region": postcode_data.get("region"),
                        "ts": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
                send_report("order", data_dump)

                return render(request, "thank_you.html", {"order_number": order_number})
        # Orders never seem to be rejected for their content
        except ParagonClientError as PCE:
            for error in PCE.args:
                logger.error("Paragon ClientError: " + error)
            raise
