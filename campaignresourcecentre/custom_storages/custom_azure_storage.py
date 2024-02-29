import logging
from urllib.parse import urlparse, urlunparse
from azure.storage.blob import ContentSettings
from django.conf import settings
from django.core.files import File
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject
from storages.backends.azure_storage import AzureStorage, clean_name
from campaignresourcecentre.custom_storages.custom_azure_file import (
    AzureMediaStorageFile,
)

logger = logging.getLogger(__name__)


class AzureMediaStorage(AzureStorage):
    account_name = getattr(settings, "AZURE_ACCOUNT_NAME", None)
    account_key = getattr(settings, "AZURE_ACCOUNT_KEY", None)
    azure_container = getattr(settings, "AZURE_CONTAINER", None)
    external_domain = getattr(settings, "AZURE_CUSTOM_DOMAIN", None)
    custom_domain = None

    # Based on Azure storage _save method
    def _move_temp_blob(
        self,
        temp_blob_name,
        new_blob_name,
        content,
    ):
        logger.info(
            "Saving %s in container %s of account %s",
            new_blob_name,
            __class__.azure_container,
            __class__.account_name,
        )
        cleaned_name = clean_name(new_blob_name)
        new_blob_name = self._get_valid_path(new_blob_name)
        params = self._get_content_settings_parameters(new_blob_name, content)
        temp_blob_client = self.client.get_blob_client(temp_blob_name)
        new_blob_client = self.client.get_blob_client(new_blob_name)

        # Copy the blob to the new name
        temp_url = temp_blob_client.url

        logger.info(
            "Copying temporary blob %s to blob %s", temp_blob_name, new_blob_name
        )
        new_blob_client.start_copy_from_url(temp_url)

        logger.info("Setting headers of blob %s to %s", new_blob_name, params)
        if params:
            new_blob_client.set_http_headers(
                ContentSettings(
                    **{
                        name: value
                        for name, value in params.items()
                        if value is not None
                    }
                )
            )

        # Delete the original blob
        logger.info("Deleting temporary blob %s", temp_blob_name)
        temp_blob_client.delete_blob()
        logger.info("Blob %s renamed to %s", temp_blob_name, new_blob_name)

        logger.info("File %s saved as %s", new_blob_name, cleaned_name)
        return cleaned_name

    def save(self, name, content, max_length=None):
        """
        Save new content to the file specified by name. The content should be
        a proper File object or any Python file-like object, ready to be read
        from the beginning.
        """
        logger.info(f"save: name={name}, content")
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name
        available_name = self.get_available_name(name, max_length=max_length)

        if not name.startswith("documents/"):
            logger.error(
                f"attempting to save blob to folder other than 'documents' - save will not take place"
            )
            return

        temp_blob_name = name[len("documents/") :]
        if self.exists(temp_blob_name):
            logger.info(
                f"_move_temp_blob: temp_blob_name={temp_blob_name}, new_blob_name={available_name}, content"
            )
            return self._move_temp_blob(temp_blob_name, available_name, content)

        if not hasattr(content, "chunks"):
            content = File(content, available_name)

        logger.info(f"_save: name={available_name}, content")
        return self._save(available_name, content)

    def __init__(self, **settings):
        super().__init__(**settings)
        logger.info("Using storage domain '%s' for media", self.custom_domain)

    def find_newest_blob_starting_with(self, name_prefix=""):
        """Return all files for a given path"""
        if name_prefix:
            name_prefix = self._get_valid_path(name_prefix)

        # XXX make generator, add start, end
        blobs_with_prefix = [
            blob for blob in self.client.list_blobs(name_starts_with=name_prefix)
        ]
        logger.info(
            f"blobs with prefix '{name_prefix}': {', '.join(map(lambda blob: blob.name, blobs_with_prefix))}"
        )

        if blobs_with_prefix:
            newest_blob = sorted(
                blobs_with_prefix, key=lambda blob: blob.last_modified, reverse=True
            )[0]
            logger.info(
                f"newest blob is '{newest_blob.name}', lastModified: '{newest_blob.last_modified}'"
            )
            return newest_blob
        else:
            return None

    def url(self, name, expire=None, parameters=None):
        initial_url = super().url(name, expire, parameters)
        components = list(urlparse(initial_url))
        components[1] = self.external_domain
        new_url = urlunparse(components)
        return new_url

    def _open(self, name, mode="rb"):
        logger.info("Opening media storage: %s %s", name, mode)
        return AzureMediaStorageFile(name, self, mode)

    def _get_valid_path(self, name):
        return self._normalize_name(clean_name(name))


# As per https://docs.djangoproject.com/en/4.1/ref/files/uploads/
class AzureSearchStorage(AzureStorage):
    account_name = getattr(settings, "AZURE_SEARCH_STORAGE_ACCOUNT_NAME", None)
    account_key = getattr(settings, "AZURE_SEARCH_ACCESS_KEY", None)
    azure_container = getattr(settings, "AZURE_SEARCH_CONTAINER", None)
    custom_domain = None

    def __init__(self, **settings):
        super().__init__(**settings)
        logger.info(
            "Using storage container %s in domain %s for search index",
            self.azure_container,
            self.custom_domain,
        )


# Based on default_storage in https://github.com/django/django/blob/main/django/core/files/storage.py
# Storage instance is only really instantiated after all settings are configured and in a request context


class SearchStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(
            getattr(settings, "SEARCH_STORAGE_CLASS", settings.DEFAULT_FILE_STORAGE)
        )()


search_storage = SearchStorage()
