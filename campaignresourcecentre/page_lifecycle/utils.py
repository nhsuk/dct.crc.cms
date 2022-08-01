import datetime
import logging
from dateutil import relativedelta
from typing import Iterable

from django.conf import settings
from django.urls import reverse

from wagtail.core.models import Site

from campaignresourcecentre.notifications import AbstractNotifications

logger = logging.getLogger(__name__)


def calculate_next_review_date(date=None):
    """Assumes `date` is a `datetime.date` object. Calculates the `next_review`
    date."""
    if date is None:
        date = datetime.date.today()
    return date + relativedelta.relativedelta(months=+get_next_review_duration())


def get_next_review_duration():
    try:
        duration_months = int(settings.PAGE_LIFECYCLE_NEXT_REVIEW_DATE_DURATION)
    except (AttributeError, ValueError):
        duration_months = 12
    return duration_months


def get_pages_for_review_notifications():
    """Fetch the page lifecycle pages that have a `next_review` date of today."""
    from campaignresourcecentre.page_lifecycle.models import PageLifecycleMixin

    # from .models import PageLifecycleMixin  # circular import (does not work in tests)

    today = datetime.date.today()
    pages = []
    for m in PageLifecycleMixin.__subclasses__():
        if m.is_creatable:
            pages.extend(m.objects.filter(next_review=today))
    return pages


def get_review_notification_email():
    from .models import PageLifecycleSettings  # circular import

    site = Site.objects.get(is_default_site=True)
    page_lifecycle_settings = PageLifecycleSettings.for_site(site)
    return getattr(page_lifecycle_settings, "notification_email")


def send_page_review_notifications(
    pages: Iterable, notifications: AbstractNotifications, notification_email=None
):
    """Send a page review due notification to the page owner of the supplied pages,
    and optionally the supplied `notification_email`.

    Args:
        pages: iterable of pages whose owners are to be notified.
        notifications: `AbstractNotifications`.
        notification_email: email address that each notifcation should be sent
            to in addition to the page owner.
    """

    for page in pages:
        recipients = []
        if notification_email:
            recipients.append(notification_email)
        if page.owner and page.owner.email:
            recipients.append(page.owner.email)
        if recipients:
            try:
                notifications.review_page(
                    recipients,
                    page.title,
                    reverse("wagtailadmin_pages:edit", args=(page.id,)),
                )
            except Exception as e:  # be more specific when email implemented
                logger.exception(str(e))
