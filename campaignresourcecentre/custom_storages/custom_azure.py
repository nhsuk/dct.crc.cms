from io import IOBase
import logging
from queue import SimpleQueue
from shutil import copyfileobj
from threading import Thread
from urllib.parse import urlparse, urlunparse
from uuid import uuid4

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobBlock, ContentSettings
from django.conf import settings
from django.core.files import File
from django.core.files.storage import get_storage_class, default_storage
from django.core.files.uploadhandler import FileUploadHandler, StopFutureHandlers
from django.core.files.uploadedfile import UploadedFile
from django.utils.functional import LazyObject

from storages.backends.azure_storage import AzureStorage, AzureStorageFile, clean_name

logger = logging.getLogger(__name__)

# Preferred block size for i/o to blobs - conforms to Azure default
DEFAULT_BLOB_BLOCK_SIZE = 1024 * 1024 * 4

# AzureStorageFile and subclasses are used when an uploaded file is needed within Django/Wagtail
# We use the default rather inefficient implementation for this to avoid coding to support e.g. r and w i/o modes
# but log usage to monitor whether this should become necessary


class AzureMediaStorageFile(AzureStorageFile):
    def _get_file(self):
        logger.info("get AzureMediaStorageFile from %s", self._blob)
        return super._get_file(self)


class AzureMediaStorage(AzureStorage):
    account_name = getattr(settings, "AZURE_ACCOUNT_NAME", None)
    account_key = getattr(settings, "AZURE_ACCOUNT_KEY", None)
    azure_container = getattr(settings, "AZURE_CONTAINER", None)
    external_domain = getattr(settings, "AZURE_CUSTOM_DOMAIN", None)
    custom_domain = None

    # Based on Azure storage _save method
    def _save(self, name, content, max_length=None):
        logger.info(
            "Saving %s in container %s of account %s",
            name,
            __class__.azure_container,
            __class__.account_name,
        )
        cleaned_name = clean_name(name)
        name = self._get_valid_path(name)
        params = self._get_content_settings_parameters(name, content)

        # Unwrap django file (wrapped by parent's save call)
        if isinstance(content, File):
            content = content.file

        saved_file = AzureBlobFile(self.client, cleaned_name, mode="wb", headers=params)
        copyfileobj(content, saved_file, DEFAULT_BLOB_BLOCK_SIZE)
        saved_file.close()
        logger.info("File %s saved as %s", name, cleaned_name)
        return cleaned_name

    def __init__(self, **settings):
        super().__init__(**settings)
        logger.info("Using storage domain '%s' for media", self.custom_domain)

    def url(self, name, expire=None, parameters=None):
        initial_url = super().url(name, expire, parameters)
        components = list(urlparse(initial_url))
        components[1] = self.external_domain
        new_url = urlunparse(components)
        return new_url

    def _open(self, name, mode="rb"):
        logger.info("Opening media storage: %s %s", name, mode)
        return AzureMediaStorageFile(name, mode, self)


class AzureDocStorage(AzureMediaStorage):
    azure_container = getattr(settings, "AZURE_DOC_CONTAINER", None)


# Class to present a Python file interface to an Azure blob.
# Surprisingly, no prior implementation seems to exist


class AzureBlobFile(IOBase):
    def __init__(
        self,
        container_client,
        blob_name,
        mode="rb",
        block_size=DEFAULT_BLOB_BLOCK_SIZE,
        destroy_on_close=False,
        headers=None,
    ):
        super().__init__()
        if mode not in ("rb", "wb"):
            raise NotImplementedError("Mode '%s' not supported for blob file" % mode)
        self.blob_name = blob_name
        self.mode = mode
        self.block_size = block_size
        self.container_client = container_client
        self.blob_client = container_client.get_blob_client(blob_name)
        self.position = 0
        self.destroy_on_close = destroy_on_close
        self.deleted = False
        self.reported_closed = False
        self.headers = {}
        if headers:
            self.headers.update(headers)

        # Used for writing. We need to write blocks one-by-one. Each block gets an id
        # that we remember in a list
        # and when all blocks are written we get Azure to concatenate the blocks into our
        # final blob
        if mode == "rb":
            blob_properties = self.blob_client.get_blob_properties()
            self.size = blob_properties.size
        else:
            self.block_buffer = bytearray(self.block_size)
            self.block_offset = 0
            self.block_list = []
            self.size = 0

    def read(self, size=-1):
        remaining = self.size - self.position
        if remaining <= 0:
            return b""
        required_length = None if size == -1 else min(size, remaining)
        result = self.blob_client.download_blob(
            offset=self.position, length=required_length
        ).read()
        self.position += len(result)
        return result

    def _write_block(self):
        if self.block_offset > 0:
            block_id = str(uuid4())
            logger.info(
                "Writing blob block %d (%s), %d byte(s) for %s",
                len(self.block_list) + 1,
                block_id,
                self.block_offset,
                self.blob_name,
            )
            try:
                self.blob_client.stage_block(
                    block_id=block_id, data=self.block_buffer[: self.block_offset + 1]
                )
                self.block_list.append(BlobBlock(block_id))
            except Exception as e:
                logger.info("Failed to write blob: %s" % e)
                raise
            self.block_offset = 0

    def write(self, data):
        data_used = 0
        while data_used < len(data):
            if self.block_offset >= self.block_size:
                self._write_block()
            block_remaining = self.block_size - self.block_offset
            block_to_use = min(block_remaining, len(data) - data_used)
            self.block_buffer[
                self.block_offset : self.block_offset + block_to_use
            ] = data[data_used : data_used + block_to_use]
            self.block_offset += block_to_use
            data_used += block_to_use
        self.position += len(data)
        self.size = self.position

    def seek(self, offset, whence=0):
        if whence == 0:
            new_position = offset
        elif whence == 1:
            new_position = self.position + offset
        elif whence == 2:
            blob_properties = self.blob_client.get_blob_properties()
            new_position = blob_properties.size + offset
        if new_position != 0 and self.mode == "wb":
            raise NotImplementedError("Can't seek to writeable blob except at offset 0")
        self.position = new_position

    def tell(self):
        return self.position

    def close(self):
        if not self.reported_closed:
            if self.mode == "wb":
                self._write_block()
                self.blob_client.commit_block_list(self.block_list)
                # Rather curiously, write blob headers after the blob itself
                if self.headers:
                    self.blob_client.set_http_headers(
                        ContentSettings(
                            **{
                                name: value
                                for name, value in self.headers.items()
                                if value is not None
                            }
                        )
                    )
                logger.info(
                    "Blob %s written as %d block(s) with headers %s",
                    self.blob_name,
                    len(self.block_list),
                    self.headers,
                )
            if self.destroy_on_close:
                logger.info("Deleting temporary blob %s", self.blob_name)
                self.delete()
            self.reported_closed = True

    def delete(self):
        if not self.deleted:
            try:
                self.blob_client.delete_blob()
                self.deleted = True
            except ResourceNotFoundError:
                logger.error(
                    "Failed to delete blob %s (does not exist)", self.blob_name
                )


# As per https://docs.djangoproject.com/en/4.1/ref/files/uploads/
class AzureBlobUploadHandler(FileUploadHandler):
    chunk_size = int(
        settings.FILE_UPLOAD_MAX_MEMORY_SIZE / 2
    )  # Half the memory size limit

    def __init__(self, *args, **kwargs):
        self.storage = default_storage
        super().__init__(*args, **kwargs)

    def new_file(
        self,
        field_name,
        file_name,
        content_type,
        content_length,
        charset=None,
        content_type_extra=None,
    ):
        super().new_file(
            field_name,
            file_name,
            content_type,
            content_length,
            charset=charset,
            content_type_extra=content_type_extra,
        )
        self.blob_name = str(uuid4())
        logger.info(
            "New file %s for AzureBlobUploadHander, blob name is %s",
            self.file_name,
            self.blob_name,
        )
        self.chunks = 0
        self.blob_file = AzureBlobFile(self.storage.client, self.blob_name, "wb")

    def receive_data_chunk(self, raw_data, start):
        self.blob_file.write(raw_data)
        self.chunks += 1
        # Returns None implicitly to signal that no later handler need process the file

    def file_complete(self, file_size):
        self.blob_file.close()
        logger.info(
            "All %d chunk(s) received, total %d byte(s)", self.chunks, file_size
        )
        self.size = file_size
        file = AzureBlobFile(
            self.storage.client, self.blob_name, "rb", destroy_on_close=True
        )
        # Handler must return a file object. However if this is a local system file
        # whether temporary or otherwise, in a K8S context it will be in memory
        # Therefore we have to return a file object that will read directly
        # from Azure storage
        return AzureUploadedFile(
            file,
            self.file_name,
            self.content_type,
            self.size,
            self.charset,
            self.content_type_extra,
        )

    def upload_complete(self):
        # This method is called by Django uploader at the wrong time. At the point
        # it is called the file has been uploaded from the client into the temporary blob,
        # but not yet saved as a document, so the temporary blob cannot yet be deleted.
        # Hence we need a 'burn this after reading' mode for the temporary blob, akin
        # to the Python temporary file that is used for file-based uploads.
        # This is implemented by the destroy_on_close property in AzureBlobFile

        # Worse still, if there are several upload handlers, this method gets called
        # even if new_file was not, so it may not even have the information it needs.
        if hasattr(self, "blob_name"):
            logger.info(
                "Upload nominally complete for %s, using blob %s",
                self.file_name,
                self.blob_name,
            )


class AzureUploadedFile(UploadedFile):
    def __init__(
        self, file, name, content_type, size, charset, content_type_extra=None
    ):
        logger.info(
            "Uploaded file %s: %s, %d byte(s), %s", name, content_type, size, charset
        )
        super().__init__(file, name, content_type, size, charset, content_type_extra)


class AzureDocStorage(AzureStorage):
    account_name = getattr(settings, "AZURE_ACCOUNT_NAME", None)
    account_key = getattr(settings, "AZURE_ACCOUNT_KEY", None)
    azure_container = getattr(settings, "AZURE_DOC_CONTAINER", None)
    external_domain = getattr(settings, "AZURE_CUSTOM_DOMAIN", None)
    custom_domain = None

    def save(self, name, content, max_length=None):
        logger.info(
            "Saving %s in container %s of account %s"
            % (name, __class__.azure_container, __class__.account_name)
        )
        return super().save(name, content, max_length)

    def __init__(self, **settings):
        super().__init__(**settings)
        logger.info("Using storage domain '%s' for Docs", self.custom_domain)

    def url(self, name, expire=7200, parameters=None):
        initial_url = super().url(name, expire, parameters)
        components = list(urlparse(initial_url))
        components[1] = self.external_domain
        new_url = urlunparse(components)
        return new_url


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


class DocStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(
            getattr(settings, "DOC_STORAGE_CLASS", settings.DEFAULT_FILE_STORAGE)
        )()


doc_storage = DocStorage()
