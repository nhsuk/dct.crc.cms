import json
import logging
from typing import Protocol

from azure.storage.blob import BlobServiceClient
from azure.common import AzureMissingResourceHttpError

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile

from campaignresourcecentre.custom_storages.custom_azure_storage import search_storage

logger = logging.getLogger(__name__)


class AbstractStorage(Protocol):
    def add_taxonomy_terms(self, taxonomy_id, taxonomy_data): ...

    def get_taxonomy_terms(self, taxonomy_id): ...

    def add_resource(self, resource_id, resource_data): ...

    def delete_resource(self, resource_id): ...


class CacheStorage:
    """Cache-based index store. Use during development/testing when Azure
    Blob Store isn't configured"""

    index_name = "Cache index"

    def add_taxonomy_terms(self, taxonomy_id, taxonomy_data):
        self._add_taxonomy_terms_to_cache(taxonomy_id, taxonomy_data)

    def get_taxonomy_terms(self, taxonomy_id):
        return self._get_taxonomy_terms_from_cache(taxonomy_id)

    def add_resource(self, resource_id, resource_data):
        self._add_resource_to_cache(resource_id, resource_data)

    def delete_resource(self, resource_id):
        self._delete_resource_from_cache(resource_id)

    def _get_taxonomy_cache_key(self, taxonomy_id):
        return f"taxonomy-{taxonomy_id}"

    def _add_taxonomy_terms_to_cache(self, taxonomy_id, data):
        logger.info(f"Adding taxonomies to cache: {taxonomy_id}")
        cache.set(self._get_taxonomy_cache_key(taxonomy_id), data, None)

    def _get_taxonomy_terms_from_cache(self, taxonomy_id):
        logger.info(f"Getting taxonomies from cache: {taxonomy_id}")
        return cache.get(self._get_taxonomy_cache_key(taxonomy_id))

    def _get_resource_cache_key(self, resource_id):
        return f"resource-{resource_id}"

    def _add_resource_to_cache(self, resource_id, resource_data):
        logger.info(f"Adding resource to cache: {resource_data}")
        cache.set(self._get_resource_cache_key(resource_id), resource_data, None)

    def _delete_resource_from_cache(self, resource_id):
        logger.info(f"Deleting resource from cache: {resource_id}")
        cache.delete(self._get_resource_cache_key(resource_id))


class AzureStorage:
    """
    Code to save index entries taken from:
    https://dev.azure.com/nhsuk/dct.sample-cms/_git/dct.wagtail-funnelback-indexer?path=%2Fwagtailfunnelbackcontentindexer%2Ftasks.py&version=GBmaster&line=160&lineEnd=161&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents
    """

    index_name = "Azure Storage index"

    def __init__(self):
        self._azure_search = settings.AZURE_SEARCH
        self._storage = search_storage
        self.added_items = set()
        self.deleted_items = set()

    def add_taxonomy_terms(self, taxonomy_id, taxonomy_data):
        pass

    def get_taxonomy_terms(self, taxonomy_id):
        pass

    def list_json_files(self):
        files = self._storage.listdir(self._storage.azure_container)
        print("Index files", files)

    def cleanup_blob_storage(self):
        files = self._storage.list_all()
        for file in files:
            self._storage.delete(file)
            logger.info("Blob deleted: %s", file)

    def add_json_file(self, name, data):
        json_file = ContentFile(json.dumps(data, indent=2).encode())
        self._storage.delete(name)
        self._storage.save(name, json_file)
        logger.info("JSON saved to file %s", name)

    def load_json_file(self, name):
        with self._storage.open(name) as json_file:
            return json.loads(json_file.read().decode())

    def add_resource(self, resource_id, resource_data):
        page_type = resource_data["resource"]["objecttype"]
        try:
            index_file_name = self._get_azure_filename(page_type, resource_id)
            resource_data["index_file_name"] = index_file_name
            index_file = ContentFile(json.dumps(resource_data).encode())
            # Remove any existing search resource blob
            self._storage.delete(index_file_name)
            self._storage.save(index_file_name, index_file)
            logger.info(
                "Blob added to index of type %s: %s" % (page_type, index_file_name)
            )
            self.added_items.add(
                (index_file_name, resource_data["resource"]["object_url"])
            )
        except Exception as err:
            logger.error("Exception raised - Azure Blob Add: %s", err)
            raise

    def delete_resource(self, resource):
        if hasattr(resource, "search_indexable"):
            self._delete_from_blob(resource)
        else:
            logger.info(
                f"'search_indexable' is not defined in {resource}, so assume no object to delete"
            )

    def _delete_from_blob(self, resource):
        index_file_name = self._get_azure_filename(resource.objecttype(), resource.id)
        try:
            self._storage.delete(index_file_name)
            logger.info("Resource index deleted: %s", resource.id)
            self.deleted_items.add(index_file_name)
        except Exception as err:
            logger.error("Exception raised - index blob Delete: %s", err)

    def _get_azure_filename(self, page_type, page_id):
        return f"asset/{page_type}_{page_id}.json"
