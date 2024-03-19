# AzureStorageFile and subclasses are used when an uploaded file is needed within Django/Wagtail
# We use the default rather inefficient implementation for this to avoid coding to support e.g. r and w i/o modes
# but log usage to monitor whether this should become necessary
# This class is only used when uploading large files - see conflunce page for details
# https://digitaltools.phe.org.uk/confluence/display/CRC/Document+Upload+to+Blob+storage

import logging
from azure.storage.blob import BlobBlock
from storages.backends.azure_storage import AzureStorageFile
from azure.core.exceptions import ResourceNotFoundError

logger = logging.getLogger(__name__)

from uuid import uuid4

# Preferred block size for i/o to blobs - conforms to Azure default
DEFAULT_BLOB_BLOCK_SIZE = 1024 * 1024 * 4


class AzureMediaStorageFile(AzureStorageFile):
    def __init__(
        self,
        blob_name,
        storage,
        mode="rb",
        block_size=DEFAULT_BLOB_BLOCK_SIZE,
        headers=None,
    ):
        if mode not in ("rb", "wb"):
            raise NotImplementedError("Mode '%s' not supported for blob file" % mode)
        self.blob_name = blob_name
        self.mode = mode
        self.block_size = block_size
        self.container_client = storage.client
        self.blob_client = storage.client.get_blob_client(blob_name)
        self.position = 0
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

    def _get_file(self):
        logger.info("get AzureMediaStorageFile from %s", self._blob)
        return super()._get_file(self)

    def delete(self):
        logger.info("deleting AzureMediaStorageFile from %s", self.blob_name)
        try:
            self.blob_client.delete_blob(self.blob_name)
        except ResourceNotFoundError:
            pass

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

    def close(self):
        if not self.reported_closed:
            if self.mode == "wb":
                self._write_block()
                self.blob_client.commit_block_list(self.block_list)
                logger.info(
                    "Blob %s written as %d block(s)",
                    self.blob_name,
                    len(self.block_list),
                )
            self.reported_closed = True
