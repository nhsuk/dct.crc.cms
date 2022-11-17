from logging import getLogger
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.baskets.exceptions import ItemNotInBasketError
from campaignresourcecentre.paragon_users.decorators import paragon_user_logged_in
from campaignresourcecentre.resources.models import ResourceItem

logger = getLogger("__name__")


@paragon_user_logged_in
@require_http_methods(["DELETE", "GET"])
def empty_basket(request):
    basket = Basket(request.session)
    basket.empty_basket()
    return redirect("/baskets/view_basket/")


def _add_item(request):
    basket = Basket(request.session)
    payload = request.POST
    try:
        # Check if a resource with this SKU exists
        item_obj = ResourceItem.objects.get(sku=payload["sku"])

        # Compose basket item object
        item_image_rendition = item_obj.image.get_rendition("width-200")
        rendition_img_attrs = item_image_rendition.attrs
        item_image_url = item_image_rendition.url
        item = {
            "id": item_obj.pk,
            "title": item_obj.title,
            "item_url": f"{item_obj.resource_page.url}",
            "item_code": item_obj.sku,
            "item_image_url": item_image_url,
            "item_img_attrs": rendition_img_attrs,
            "image_url": item_obj.image.file.url,
            "image_alt_text": item_obj.image_alt_text,
            "max_quantity": item_obj.maximum_order_quantity,
            # Look like a resource object if necessary
            "maximum_order_quantity": item_obj.maximum_order_quantity,
            "sku": item_obj.sku,
            "campaign": item_obj.campaign,
            "resource_page_id": item_obj.resource_page.id,
        }
        basket.add_item(item, payload.get("order_quantity"))
        item["items_in_basket_count"] = basket.get_item_count(item_obj.pk)
        return item
    except Exception as e:
        logger.error("Failed to find resource item: %s", e)
        raise SuspiciousOperation


@paragon_user_logged_in
@require_http_methods(["POST"])
def add_item(request):
    item_obj = _add_item(request)
    return redirect(item_obj["item_url"])


@paragon_user_logged_in
@require_http_methods(["POST"])
def render_resource_basket(request):
    item_obj = _add_item(request)
    return render(
        request, "molecules/baskets/resource_basket.html", {"resource": item_obj}
    )


@paragon_user_logged_in
@require_http_methods(["GET"])
def view_basket(request):
    basket = Basket(request.session)
    items = basket.get_all_items().items()
    result = render(
        request,
        "view_basket.html",
        {"items": items, "has_errors": basket.has_errors},
    )
    return result


@paragon_user_logged_in
@require_http_methods(["POST"])
def change_item_quantity(request):
    _change_item_quantity(request)
    return redirect("/baskets/view_basket/")


def _change_item_quantity(request):
    basket = Basket(request.session)
    payload = request.POST
    try:
        item_id = int(payload["item_id"])
        return basket.change_item_quantity(item_id, payload.get("order_quantity"))
    except Exception as e:
        logger.error("Change item quantity error. Payload: %s", payload)
    raise SuspiciousOperation


@paragon_user_logged_in
@require_http_methods(["POST"])
def render_basket(request):
    item = _change_item_quantity(request)
    return render(request, "molecules/baskets/basket.html", {"item": item})


@paragon_user_logged_in
@require_http_methods(["GET"])
def render_basket_errors(request):
    basket = Basket(request.session)
    r = request.GET.get("r")
    if r:
        try:
            id = int(r)
            items = basket.get_resource_page_items(id).items()
        except ValueError:
            raise SuspiciousOperation
    else:
        items = basket.get_all_items().items()

    error_count = sum(
        (
            1 if (item[1].get("no_quantity") or item[1].get("bad_quantity")) else 0
            for item in items
        )
    )
    return render(
        request,
        "molecules/baskets/basket_errors.html",
        {
            "items": items,
            "has_errors": error_count > 0,
        },
    )


@paragon_user_logged_in
@require_http_methods(["POST"])
def remove_item(request):
    _remove_item(request)
    return redirect("/baskets/view_basket/")


@paragon_user_logged_in
@require_http_methods(["POST"])
def _remove_item(request):
    basket = Basket(request.session)
    payload = request.POST
    try:
        item_id = int(payload["item_id"])
        basket.remove_item(item_id)
    except Exception as e:
        logger.error("Remove item error. Payload: %s", payload)
        raise SuspiciousOperation


@paragon_user_logged_in
@require_http_methods(["POST"])
def render_remove_item(request):
    _remove_item(request)
    basket = Basket(request.session)
    items = basket.get_all_items().items()
    return render(
        request,
        "molecules/baskets/basket_checkout.html",
        {
            "items": items,
        },
    )
