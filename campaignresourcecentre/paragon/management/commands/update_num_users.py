import logging

from django.core.management.base import BaseCommand

from campaignresourcecentre.paragon.models import ParagonCacheValues
from campaignresourcecentre.paragon.helpers.users import get_current_num_users

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command finds the current number of Paragon users and updates
    the cached value.

    This should be run periodically (every few minutes) to ensure
    that the Paragon users in Wagtail admin shows the latest users.
    """

    def handle(self, *args, **options):
        logger.info('Fetching current number of users')
        paragon_cache_values = ParagonCacheValues.load()
        num_users = get_current_num_users(paragon_cache_values.num_users)
        paragon_cache_values.num_users = num_users
        paragon_cache_values.save()
