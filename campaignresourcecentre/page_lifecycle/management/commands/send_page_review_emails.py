from django.core.management.base import BaseCommand

from campaignresourcecentre.notifications import gov_notify_factory

from ...utils import (
    get_pages_for_review_notifications,
    get_review_notification_email,
    send_page_review_notifications,
)


class Command(BaseCommand):
    help = "Sends an email to the appropriate users regarding pages that need "
    "to be reviewed."

    def handle(self, *args, **options):
        notification_email = get_review_notification_email()
        notifications = gov_notify_factory()
        pages = get_pages_for_review_notifications()
        send_page_review_notifications(pages, notifications, notification_email)
