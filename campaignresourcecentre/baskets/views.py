from logging import getLogger
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.baskets.exceptions import ItemNotInBasketError

from campaignresourcecentre.resources.models import ResourceItem

logger = getLogger ("__name__")

@require_http_methods(["DELETE", "GET"])
def empty_basket(request):
    basket = Basket(request.session)
    basket.empty_basket()
    return redirect("/baskets/view_basket/")

def _add_item(request):
    basket = Basket(request.session)
    payload = request.POST
    try:
        # Check if either of sku and quantity provided is dodgy
        item_obj = ResourceItem.objects.get(sku=payload["sku"])
        if not "order_quantity" in payload:
            logger.error ("No order quantity")
            raise SuspiciousOperation
        order_quantity_text = payload ["order_quantity"]
        if not order_quantity_text.isdigit ():
            logger.error ("Non-numeric order quantity: '%s'", order_quantity_text)
            raise SuspiciousOperation
        # Compose basket item object
        item_image_rendition = item_obj.image.get_rendition("width-200")
        rendition_img_attrs = item_image_rendition.attrs
        item_image_url = item_image_rendition.url
        item = {
            "id": item_obj.pk,
            "title": item_obj.title,
            "item_url": f'{item_obj.resource_page.url}',
            "item_code": item_obj.sku,
            "item_image_url": item_image_url,
            "item_img_attrs": rendition_img_attrs,
            "image_url": item_obj.image.file.url,
            "image_alt_text": item_obj.image_alt_text,
            "max_quantity": item_obj.maximum_order_quantity,
        }
        basket.add_item(item, int(order_quantity_text))
        item["items_in_basket_count"] =  basket.get_item_count(item_obj.pk)
        item["sku"] = item_obj.sku
        # maximum_order_quantity seems to duplicate max_quantity - refactor ?
        item["maximum_order_quantity"] = item_obj.maximum_order_quantity
        return item
    except Exception as e:
        logger.error ("Failed to find resource item: %s", e)
        raise SuspiciousOperation

@require_http_methods(["POST"])
def add_item(request):
    item_obj = _add_item(request)
    return redirect(item_obj ["item_url"])

@require_http_methods(["POST"])
def render_resource_basket(request):
    item_obj = _add_item(request)
    return render(
        request,
        "molecules/baskets/resource_basket.html", {
            "resource": item_obj
        }
    )

@require_http_methods(["GET"])
def view_basket(request):
    if request.session.get ("ParagonUser"):
        basket = Basket(request.session)
        items = basket.get_all_items().items()
        return render(
            request,
            "view_basket.html", {
                "items": items
            }
        )
    else:
        return redirect ("/login/")

@require_http_methods(["POST"])
def change_item_quantity(request):
    _change_item_quantity(request)
    return redirect("/baskets/view_basket/")

def _change_item_quantity(request):
    basket = Basket(request.session)
    payload = request.POST
    try:
        item_id = int(payload["item_id"])
        item = basket.get_item (item_id)
        if item is not None and "order_quantity" in payload:
            quantity = int(payload["order_quantity"])
            basket.change_item_quantity(item_id, quantity)
            result = item.copy ()
            result ["updated"] = True
            return result
        else:
            logger.error ("Invalid basket item. Payload: %s", payload)
    except Exception as e:
        logger.error ("Change item quantity error. Payload: %s", payload)
    raise SuspiciousOperation

@require_http_methods(["POST"])
def render_basket(request):
    item = _change_item_quantity(request)
    return render(
        request,
        "molecules/baskets/basket.html", {
            "item": item
        }
    )

@require_http_methods(["POST"])
def render_basket_errors(request):
    item = _change_item_quantity(request)
    return render(
        request,
        "molecules/baskets/basket_errors.html", {
            "item": item
        }
    )

@require_http_methods(["POST"])
def remove_item(request):
    basket = Basket(request.session)
    payload = request.POST
    try:
        item_id = int(payload["item_id"])
        basket.remove_item(item_id)
    except Exception as e:
        logger.error ("Remove item error. Payload: %s", payload)
        raise SuspiciousOperation

    return redirect("/baskets/view_basket/")
