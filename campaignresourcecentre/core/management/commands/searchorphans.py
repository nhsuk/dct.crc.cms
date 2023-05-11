import json
import logging
import re
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from campaignresourcecentre.azurestore.utils import AzureStorage
from campaignresourcecentre.search.azure import AzureSearchBackend

logger = logging.getLogger(__name__)


def process_orphans(orphans, url_re, process_dup):
    for orphan_url, orphan_dups in sorted(orphans.items()):
        for orphan in orphan_dups:
            data = orphan["content"]["resource"]
            label = f"{data ['objecttype']} {orphan_url}"
            if url_re is None or url_re.match(data["object_url"]):
                process_dup(label, orphan)


class Command(BaseCommand):
    def _process_orphan_dup(self, label, orphan, deleting):
        if deleting:
            try:
                self.backend.delete_search_resource(orphan)
                self.stdout.write(f"{label}{' deleted' if deleting else ''}")
            except Exception as e:
                self.stdout.write(f"failed to delete {label}: {e}")
        else:
            self.stdout.write(f"{label}")

    def handle(self, *args, **kwargs):
        self.storage = AzureStorage()
        self.backend = AzureSearchBackend({})
        deleting = kwargs.get("delete")
        url_re = re.compile(kwargs["urls"]) if kwargs.get("urls") else None
        try:
            orphans = self.storage.load_json_file(
                f"orphans_{AzureStorage.index_name}.json"
            )
            process_orphans(
                orphans,
                url_re,
                lambda label, orphan: self._process_orphan_dup(label, orphan, deleting),
            )
        except Exception as e:
            self.stderr.write(f"Couldn't process orphans: {e}")

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            default=False,
            help="Delete orphan objects from the index",
        )
        parser.add_argument(
            "--urls", dest="urls", help="Use only objects matching a pattern"
        )
