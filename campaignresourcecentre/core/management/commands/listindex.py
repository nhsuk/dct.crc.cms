import json
import logging
import re
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from campaignresourcecentre.azurestore.utils import AzureStorage
from campaignresourcecentre.search.azure import AzureSearchBackend

logger = logging.getLogger(__name__)


def process_files(filepaths, url_re, process_file):
    for filepath in sorted(filepaths):
        if url_re is None or url_re.match(filepath):
            process_file(filepaths)


class Command(BaseCommand):
    def _process_file(self, filename, deleting):
        if deleting:
            try:
                # self.backend.delete_search_resource(orphan)
                self.stdout.write(f"{filename}{' deleted' if deleting else ''}")
            except Exception as e:
                self.stdout.write(f"failed to delete {filename}: {e}")
        else:
            self.stdout.write(f"{fiename}")

    def handle(self, *args, **kwargs):
        self.storage = AzureStorage()
        self.backend = AzureSearchBackend({})
        deleting = kwargs.get("delete")
        url_re = re.compile(kwargs["urls"]) if kwargs.get("urls") else None
        try:
            _, filenames = self.storage.listdir("asset")
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
