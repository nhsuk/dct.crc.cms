import json
import logging
import re
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from campaignresourcecentre.azurestore.utils import AzureStorage, CacheStorage
from campaignresourcecentre.search.azure import AzureSearchBackend

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        storage = AzureStorage()
        backend = AzureSearchBackend({})
        deleting = kwargs["delete"]
        url_re = re.compile(kwargs["urls"]) if kwargs["urls"] else None
        try:
            orphans = storage.load_json_file(f"orphans_{AzureStorage.index_name}.json")
            for orphan_url, orphan_dups in sorted(orphans.items()):
                for orphan in orphan_dups:
                    data = orphan["content"]["resource"]
                    if url_re is None or url_re.match(data["object_url"]):
                        if deleting:
                            try:
                                backend.delete_search_resource(orphan)
                                self.stdout.write(
                                    f"{data ['objecttype']} {orphan_url}{' deleted' if deleting else ''}"
                                )
                            except Exception as e:
                                self.stdout.write(
                                    f"failed to delete {data ['objecttype']} {orphan_url}: {e}"
                                )
                        else:
                            self.stdout.write(f"{data ['objecttype']} {orphan_url}")
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
