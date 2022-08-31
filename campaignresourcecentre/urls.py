from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView, RedirectView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns

from campaignresourcecentre.search import views as search_views
from campaignresourcecentre.users import admin_views as user_admin_views
from campaignresourcecentre.utils.cache import get_default_cache_control_decorator
from campaignresourcecentre.paragon_users.views import (
    order_history,
    signup,
    login,
    verification,
    password_reset,
    password_set,
    logout,
    user_profile,
    newsletter_preferences,
    resend_verification,
)
from campaignresourcecentre.baskets import views as basket_views
from campaignresourcecentre.orders import views as orders_views
from campaignresourcecentre.resources import views as resource_views
from campaignresourcecentre.campaigns import views as campaign_views
from campaignresourcecentre.standardpages import views as standardpages_views
from campaignresourcecentre.standardpages.views import (
    contact_us,
    thank_you,
    clear_cache,
    session_summary,
    cookie_confirmation,
    cookie_settings,
    update_index,
)

from logging import getLogger

logger = getLogger(__name__)

# Private URLs are not meant to be cached.
private_urlpatterns = [
    path("crc-django-admin/", admin.site.urls),
    path("crc-admin/password_reset/", user_admin_views.PasswordResetView.as_view()),
    path("crc-admin/clear_cache/", clear_cache, name="clear_cache"),
    path("crc-admin/update_index/", update_index, name="update_index"),
    path("crc-admin/", include(wagtailadmin_urls)),
    path("crc-documents/", include(wagtaildocs_urls)),
    path("verification/", verification, name="verification"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("password-reset/", password_reset, name="password-reset"),
    path("password-set/", password_set, name="password-set"),
    path("logout/", logout, name="logout"),
    path("account/", user_profile, name="account"),
    path("session/summary", session_summary, name="session_summary"),
    path("account/newsletters/", newsletter_preferences, name="newsletter_preferences"),
    path("account/orders/", order_history, name="order_history"),
    path("account/reverification/", resend_verification, name="resend_verification"),
    path("baskets/empty/", basket_views.empty_basket, name="empty_basket"),
    path("baskets/add_item/", basket_views.add_item, name="add_item"),
    path(
        "baskets/render_resource_basket/",
        basket_views.render_resource_basket,
        name="render_resource_basket",
    ),
    path("baskets/render_basket/", basket_views.render_basket, name="render_basket"),
    path(
        "baskets/render_basket_errors/",
        basket_views.render_basket_errors,
        name="render_basket_errors",
    ),
    path(
        "baskets/change_item_quantity/",
        basket_views.change_item_quantity,
        name="change_item_quantity",
    ),
    path("baskets/remove_item/", basket_views.remove_item, name="remove_item"),
    path(
        "baskets/render_remove_item/",
        basket_views.render_remove_item,
        name="render_remove_item"
    ),
    path("baskets/view_basket/", basket_views.view_basket, name="view_basket"),
    path("orders/place_order/", orders_views.place_order, name="place_order"),
    path("orders/summary/", orders_views.summary, name="order_summary"),
    path("orders/address/edit/", orders_views.delivery_address, name="order_summary"),
    path("orders/place/", orders_views.place_order, name="place_order"),
    path("search/", resource_views.search, name="resource_search"),
    path("render_search/", resource_views.render_search, name="render_search"),
    path("render_topic/", campaign_views.render_topic, name="render_topic"),
    path("contact-us/", contact_us, name="contact_us"),
    path("thank_you/", thank_you, name="thank_you"),
    path("cookies/", standardpages_views.cookie_declaration, name="cookies"),
    path(
        "cookie_settings/", standardpages_views.cookie_settings, name="cookie_settings"
    ),
    path(
        "cookie_confirmation/",
        standardpages_views.cookie_confirmation,
        name="cookie_confirmation",
    ),
]
private_urlpatterns = decorate_urlpatterns(private_urlpatterns, never_cache)

# Search cache-control headers are set on the view itself.
private_urlpatterns += (path("crc-search/", search_views.search, name="search"),)

# Public URLs that are meant to be cached.
urlpatterns = [
    path("sitemap.xml", sitemap),
]

# Set vary header to instruct cache to serve different version on different
# encodings, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers("X-Requested-With", "X-Forwarded-Proto", "Accept-Encoding"),
)
# Not all pages with cookies present are uncachable, only pages setting cookies,
# so we don't specify Cookie in the Vary_On header,
# instead this decision is made in middleware

# Set public URLs to use the "default" cache settings.
urlpatterns = decorate_urlpatterns(urlpatterns, get_default_cache_control_decorator())

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    debug_urlPatterns = []
    # Serve static and media files from development server
    debug_urlPatterns += staticfiles_urlpatterns()
    debug_urlPatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    debug_urlPatterns += [
        # Add views for testing 400, 404 and 500 templates
        path(
            "test400/",
            TemplateView.as_view(template_name="errors/400.html"),
        ),
        path(
            "test404/",
            TemplateView.as_view(template_name="errors/404.html"),
        ),
        path(
            "test500/",
            TemplateView.as_view(template_name="errors/500.html"),
        ),
    ]

    # Try to install the django debug toolbar, if exists
    if apps.is_installed("debug_toolbar"):
        import debug_toolbar

        debug_urlPatterns = [
            path("__debug__/", include(debug_toolbar.urls))
        ] + debug_urlPatterns
    decorate_urlpatterns(debug_urlPatterns, never_cache)
    urlpatterns = debug_urlPatterns + urlpatterns

# Join private and public URLs.
urlpatterns = (
    private_urlpatterns
    + urlpatterns
    + [
        # Add Wagtail URLs at the end.
        # Wagtail cache-control is set on the page models's serve methods.
        path("", include(wagtail_urls))
    ]
)

# Error handlers
handler400 = "campaignresourcecentre.utils.views.bad_request"
handler403 = "campaignresourcecentre.utils.views.forbidden"
handler404 = "campaignresourcecentre.utils.views.page_not_found"
handler500 = "campaignresourcecentre.utils.views.server_error"
