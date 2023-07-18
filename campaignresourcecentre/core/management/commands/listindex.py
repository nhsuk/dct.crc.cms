import json
import logging
import re
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from campaignresourcecentre.azurestore.utils import AzureStorage

logger = logging.getLogger(__name__)


def process_files(filenames, url_re, process_file):
    for filename in sorted(filenames):
        if url_re is None or url_re.match(filename):
            process_file(filename)


class Command(BaseCommand):
    def _process_file(self, filename, deleting):
        filepath = "/asset/%s" % filename
        if deleting:
            try:
                self.storage._storage.delete(filepath)
                self.stdout.write(f"{filepath} deleted")
            except Exception as e:
                self.stdout.write(f"failed to delete {filepath}: {e}")
        else:
            self.stdout.write(f"{filepath}")

    def handle(self, *args, **kwargs):
        self.storage = AzureStorage()
        deleting = kwargs.get("delete")
        try:
            url_re = re.compile(kwargs["urls"]) if kwargs.get("urls") else None
            _, filenames = self.storage._storage.listdir("/asset")
            process_files(
                filenames,
                url_re,
                lambda filename: self._process_file(filename, deleting),
            )
        except Exception as e:
            self.stderr.write(f"Couldn't process filenames: {e}")

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            default=False,
            help="Delete search object files ifrom Azure container",
        )
        parser.add_argument(
            "--urls", dest="urls", help="Use only filenames matching a pattern"
        )
