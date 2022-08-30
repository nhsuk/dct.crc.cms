# This middleware has two purposes:

# (1) Construct an X-CRC-SESSION response header identifying the varying properties of the page so they can be cached externally
# (2) Add the X-CRC-SESSION header to the response VARY header

# Notes

# (1) This middleware must PRECEDE other caching middleware
# (2) Django site-wide caching should now work

import logging

from django.middleware.cache import UpdateCacheMiddleware, FetchFromCacheMiddleware
from django.utils.cache import (
    patch_vary_headers,
    get_cache_key,
    add_never_cache_headers,
)
from django.utils.regex_helper import _lazy_re_compile

from campaignresourcecentre.baskets.basket import Basket

cc_delim_re = _lazy_re_compile(r"\s*,\s*")
campaign_page_re = _lazy_re_compile(r"/campaigns/[^\/]+/?$")

logger = logging.getLogger(__name__)


def remove_vary_headers(response, headersToRemove):
    existingHeaders = response.get("Vary")
    if existingHeaders:
        vary_headers = [
            headerName
            for headerName in cc_delim_re.split(existingHeaders)
            if headerName not in headersToRemove
        ]
        if vary_headers:
            response["Vary"] = ", ".join(vary_headers)
        else:
            del response["Vary"]


def is_cacheable(request, response, path):
    cc = response.get("Cache-Control", ())
    # Don't cache pages explicitly marked as non-cacheable
    if cc and "private" in cc:
        return False
    # Don't cache any page rendered for a logged-in Django/Wagtail user
    if hasattr(request, "user") and request.user.is_authenticated:
        return False
    # The following condition should match all Wagtail-managed URLs that may be cached
    # i.e. they have no session-specific content or headers - i.e. no forms with their CSRF tokens
    return path in ("/", "/campaigns/") or (campaign_page_re.match(path) is not None)


class CRCUpdateCacheMiddleware(UpdateCacheMiddleware):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        path = request.get_full_path()
        canCache = is_cacheable(request, response, path)
        if canCache:
            if len(response.cookies):
                logger.info(
                    "Potentially cachable page %s set cookies %s",
                    path,
                    sorted(response.cookies.keys()),
                )
                add_never_cache_headers(response)
            else:
                remove_vary_headers(response, ["Cookie"])
        else:
            add_never_cache_headers(response)
        response = super().process_response(request, response)
        logger.debug("Update process response for %s, cachable %s", path, canCache)

        return response


class CRCFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):

        response = super().process_request(request)

        if response is not None:
            path = request.get_full_path()
            logger.debug("Cache entry available for page %s", path)
            # Any page setting cookies should not have been cached
            if len(response.cookies):
                logger.error(
                    "Cached page %s set cookies %s",
                    path,
                    sorted(response.cookies.items()),
                )
                raise Exception("Cached page set cookies")
            # Don't serve any cached page to a Django/Wagtail user
            if hasattr(request, "user") and request.user.is_authenticated:
                logger.debug(
                    "Discarding cache entry for %s requested by %s",
                    path,
                    request.user.username,
                )
                response = None

        return response
