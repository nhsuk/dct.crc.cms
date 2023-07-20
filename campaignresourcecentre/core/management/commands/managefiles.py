import json
import logging
import re
import requests

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from azure.storage.blob import ContentSettings

from campaignresourcecentre.azurestore.utils import AzureStorage

logger = logging.getLogger(__name__)


def process_files(filenames, url_re, process_file):
    for filename in sorted(filenames):
        if url_re is None or url_re.match(filename):
            process_file(filename)


class Command(BaseCommand):
    def _process_file(self, filename, deleting, patching):
        filepath = "/%s/%s" % (self.folder, filename)
        if self.folder == "assets":
            if deleting:
                try:
                    self.storage.delete(filepath)
                    self.stdout.write(f"{filepath} deleted")
                except Exception as e:
                    self.stdout.write(f"failed to delete {filepath}: {e}")
            else:
                self.stdout.write(f"{filepath}")
        else:
            self.stdout.write(f"{filepath}")
            if self.client:
                blob_client = self.client.get_blob_client(filepath[1:])
                blob_properties = blob_client.get_blob_properties()
                settings = blob_properties["content_settings"]
                content_type = settings.get("content_type")
                if content_type:
                    if content_type.startswith("{"):
                        self.stdout.write("Bad content type: %s" % content_type)
                        jsonized_content_type = content_type.replace("'", '"').replace(
                            "None", "null"
                        )
                        self.stdout.write("JSONized as %s" % jsonized_content_type)
                        if patching:
                            faulty = {
                                name: value
                                for name, value in json.loads(
                                    jsonized_content_type
                                ).items()
                                if value is not None
                            }
                            blob_client.set_http_headers(
                                content_settings=ContentSettings(**faulty)
                            )
                            self.stdout.write(
                                "Content type headers rewritten as %s" % faulty
                            )
                    else:
                        self.stdout.write("Content type: %s" % content_type)
                else:
                    self.stdout.write("Missing content type: %s", filepath)

    def handle(self, *args, **kwargs):
        if kwargs["storage"] == "search":
            self.folder = "asset"
            self.storage = AzureStorage()._storage
        else:
            self.folder = "documents"
            self.storage = default_storage
        # Azure storage specific code - file storage is used in tests
        # which has no client attribute
        self.client = getattr(self.storage, "client", None)
        deleting = kwargs.get("delete")
        patching = kwargs.get("patch")
        try:
            url_re = re.compile(kwargs["urls"]) if kwargs.get("urls") else None
            _, filenames = self.storage.listdir("/%s" % self.folder)
            process_files(
                filenames,
                url_re,
                lambda filename: self._process_file(filename, deleting, patching),
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
            "--patch-properties",
            action="store_true",
            dest="patch",
            default=False,
            help="Repair content-type property headers where corrupted",
        )
        parser.add_argument(
            "--urls", dest="urls", help="Use only filenames matching a pattern"
        )
        parser.add_argument(
            "--storage",
            dest="storage",
            help="Choose media or search (default search)",
            default="search",
            choices=["documents", "search"],
        )
