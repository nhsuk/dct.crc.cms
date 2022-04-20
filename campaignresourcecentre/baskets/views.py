from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.conf import settings

from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.resources.models import ResourceItem

@require_http_methods(["DELETE", "GET"])
def empty_basket(request):
    basket = Basket(request.session)
    basket.empty_basket()
    return redirect("/baskets/view_basket/")

def _add_item(request):
    basket = Basket(request.session)
    payload = request.POST
    item_obj = ResourceItem.objects.get(sku=payload["sku"])
    if item_obj and payload["order_quantity"]:
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
        basket.add_item(item, int(payload["order_quantity"]))
        item["items_in_basket_count"] =  basket.get_item_count(item_obj.pk)
        item["sku"] = item_obj.sku
        item["maximum_order_quantity"] = item_obj.maximum_order_quantity
        return item

@require_http_methods(["POST"])
def add_item(request):
    payload = request.POST
    item_obj = ResourceItem.objects.get(sku=payload["sku"])
    _add_item(request)
    return redirect(item_obj.resource_page.url)

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

@require_http_methods(["POST"])
def _change_item_quantity(request):
    basket = Basket(request.session)
    payload = request.POST
    item_id = int(payload["item_id"])
    quantity = int(payload["order_quantity"])
    max_quantity = basket.get_max_quantity(item_id)
    basket.change_item_quantity(item_id, quantity)
    return {
        "id": item_id,
        "quantity": quantity,
        "max_quantity": max_quantity,
    }

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
def remove_item(request):
    basket = Basket(request.session)
    payload = request.POST
    item_id = int(payload["item_id"])
    basket.remove_item(item_id)
    
    return redirect("/baskets/view_basket/")
