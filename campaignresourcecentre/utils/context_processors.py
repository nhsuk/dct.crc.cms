from django.conf import settings

from campaignresourcecentre.utils.models import Tracking
from campaignresourcecentre.baskets.basket import Basket


def global_vars(request):
    tracking = Tracking.for_request(request)
    basket = Basket(request.session)
    return {
        "GOOGLE_TAG_MANAGER_ID": getattr(tracking, "google_tag_manager_id", None),
        "SEO_NOINDEX": settings.SEO_NOINDEX,
        "BASKET_ITEM_COUNT": basket.get_items_count(),
        "CANONICAL_PATH": request.build_absolute_uri(request.path),
    }
