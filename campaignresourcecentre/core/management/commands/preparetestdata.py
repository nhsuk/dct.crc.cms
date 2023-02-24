# Django command to ensure there is minimal content in a new CRC Wagtail database for systematic testing

# Idempotent - should make no changes if it has already been run or if the
# named content is already present from manual editing

# after containers started:

# dj migrate
# dj preparetestdata
# djrun

from django.core.management.base import BaseCommand

from campaignresourcecentre.core.preparetestdata import PrepareTestData


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # The root Page and a default homepage are created by wagtail migrations
        # This command should be idempotent, i.e. it will leave pages intact if they exist already
        self._verbosity = kwargs["verbosity"]

        PrepareTestData()

        if self._verbosity > 0:
            msg = "Test pages successfully created."
            self.stdout.write(msg)
