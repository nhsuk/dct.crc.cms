# This class is only used when uploading large files - see conflunce page for details
# https://digitaltools.phe.org.uk/confluence/display/CRC/Document+Upload+to+Blob+storage

import logging
import json
from django.core.files.uploadedfile import UploadedFile
from io import BytesIO
from campaignresourcecentre.custom_storages.custom_azure_file import (
    AzureMediaStorageFile,
)
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadhandler import FileUploadHandler


from datetime import datetime

logger = logging.getLogger(__name__)


# As per https://docs.djangoproject.com/en/4.1/ref/files/uploads/
class AzureUploadedFile(UploadedFile):
    def __init__(
        self,
        upload_metadata_dict,
        name,
        content_type,
        size,
        charset,
        content_type_extra=None,
    ):
        metadata = json.dumps(upload_metadata_dict, indent=4)
        logger.info(
            "Uploaded file %s: %s, %d byte(s), %s", name, content_type, size, metadata
        )
        bytes = str.encode(metadata)
        super().__init__(
            BytesIO(bytes), name, content_type, size, charset, content_type_extra
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
        self.upload_start_time = datetime.utcnow()
        super().new_file(
            field_name,
            file_name,
            content_type,
            content_length,
            charset=charset,
            content_type_extra=content_type_extra,
        )

        end_blob_name = self.storage.get_available_name(f"documents/{file_name}")
        self.blob_name = end_blob_name[len("documents/") :]
        logger.info(
            "New file %s for AzureBlobUploadHander, temp blob name is %s, final blob name will be %s",
            self.file_name,
            self.blob_name,
            end_blob_name,
        )
        self.chunks = 0
        self.blob_file = AzureMediaStorageFile(self.blob_name, self.storage, "wb")

    def receive_data_chunk(self, raw_data, start):
        self.blob_file.write(raw_data)
        self.chunks += 1
        # Returns None implicitly to signal that no later handler need process the file

    def file_complete(self, file_size):
        upload_temp_time = datetime.utcnow()
        self.blob_file.close()
        logger.info(
            "All %d chunk(s) received, total %d byte(s)", self.chunks, file_size
        )
        blob_client = self.storage.client.get_blob_client(self.blob_name)
        temp_url = blob_client.url

        # Handler must return an UploadedFile object. To avoid having to download the blob
        # from Azure storage again to provide its content to an "UploadedFile", we have
        # created our own subclass that takes content which just references the blob.
        upload_metadata_dict = {
            "temp_url": temp_url,
            "size": file_size,
            "temp_upload_duration": f"{(upload_temp_time - self.upload_start_time).total_seconds():.3f}s",
        }

        return AzureUploadedFile(
            upload_metadata_dict,
            self.blob_name,
            self.content_type,
            file_size,
            self.charset,
            self.content_type_extra,
        )

    def upload_complete(self):
        # This method is called by Django uploader at the wrong time. At the point
        # it is called the file has been uploaded from the client into the temporary blob,
        # but not yet saved as a document, so the temporary blob cannot yet be deleted.

        # Worse still, if there are several upload handlers, this method gets called
        # even if new_file was not, so it may not even have the information it needs.
        if hasattr(self, "blob_name"):
            logger.info(
                "Upload nominally complete for %s, using blob %s",
                self.file_name,
                self.blob_name,
            )
