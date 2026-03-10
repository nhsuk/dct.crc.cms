from functools import wraps
import logging

from django.http import Http404
from wagtail.models import Site

from campaignresourcecentre.utils.models import FeatureFlags

logger = logging.getLogger(__name__)


def _get_feature_flags(request=None, site=None):
    try:
        if request is not None:
            return FeatureFlags.for_request(request)
        if site is None:
            site = Site.objects.filter(is_default_site=True).first()
        if site is None:
            return None
        return FeatureFlags.for_site(site)
    except (Site.DoesNotExist, FeatureFlags.DoesNotExist):
        return None
    except Exception as error:
        logger.exception(error)
        return None


def is_ordering_and_checkout_disabled(request=None, site=None):
    flags = _get_feature_flags(request=request, site=site)
    return bool(flags and flags.disable_ordering_and_checkout)


def is_order_history_disabled(request=None, site=None):
    flags = _get_feature_flags(request=request, site=site)
    return bool(flags and flags.disable_order_history)


def require_ordering_enabled(view_func):
    @wraps(view_func)
    def _wrapped(*args, **kwargs):
        request = args[0]
        if is_ordering_and_checkout_disabled(request=request):
            raise Http404
        return view_func(*args, **kwargs)

    return _wrapped


def require_order_history_enabled(view_func):
    @wraps(view_func)
    def _wrapped(*args, **kwargs):
        request = args[0]
        if is_order_history_disabled(request=request):
            raise Http404
        return view_func(*args, **kwargs)

    return _wrapped
