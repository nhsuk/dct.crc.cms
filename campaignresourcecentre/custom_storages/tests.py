import io
import unittest
from unittest.mock import MagicMock, patch

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobProperties

from django.conf import settings
from django.core.files.storage import default_storage


from campaignresourcecentre.custom_storages.custom_azure import (
    AzureBlobFile,
    AzureBlobUploadHandler,
    AzureUploadedFile,
)


TEST_CONTENT = b"test_content"


class TestAzureBlobFile(unittest.TestCase):
    def setUp(self):
        self.container_client = MagicMock()
        self.blob_client = MagicMock()
        self.container_client.get_blob_client.return_value = self.blob_client
        self.blob_input_file = AzureBlobFile(
            self.container_client, "test_blob_in", mode="rb"
        )
        self.blob_output_file = AzureBlobFile(
            self.container_client, "test_blob_out", mode="wb"
        )
        self.temporary_blob_file = AzureBlobFile(
            self.container_client, "test_blob_in", destroy_on_close=True
        )

    def test_init(self):
        self.assertEqual(self.blob_input_file.blob_name, "test_blob_in")
        self.assertEqual(self.blob_input_file.mode, "rb")
        self.assertEqual(self.blob_input_file.block_size, 4194304)
        self.assertEqual(self.blob_input_file.container_client, self.container_client)
        self.assertEqual(self.blob_input_file.blob_client, self.blob_client)
        self.assertEqual(self.blob_input_file.position, 0)
        self.assertFalse(self.blob_input_file.destroy_on_close)
        self.assertFalse(self.blob_input_file.deleted)
        self.assertFalse(self.blob_input_file.reported_closed)
        self.assertEqual(self.blob_output_file.blob_name, "test_blob_out")
        self.assertEqual(self.blob_output_file.mode, "wb")
        self.assertEqual(self.blob_output_file.block_size, 4194304)
        self.assertEqual(self.blob_output_file.container_client, self.container_client)
        self.assertEqual(self.blob_output_file.blob_client, self.blob_client)
        self.assertEqual(self.blob_output_file.position, 0)
        self.assertFalse(self.blob_output_file.destroy_on_close)
        self.assertFalse(self.blob_output_file.deleted)
        self.assertFalse(self.blob_output_file.reported_closed)

    def test_init_with_wb_mode(self):
        self.assertEqual(self.blob_output_file.block_buffer, bytearray(4194304))
        self.assertEqual(self.blob_output_file.block_offset, 0)
        self.assertEqual(self.blob_output_file.block_list, [])
        self.assertEqual(self.blob_output_file.size, 0)

    def test_init_with_invalid_mode(self):
        with self.assertRaises(NotImplementedError):
            AzureBlobFile(self.container_client, "test_blob", mode="invalid")

    def test_write(self):
        self.blob_output_file.write(TEST_CONTENT)
        self.assertEqual(self.blob_output_file.position, len(TEST_CONTENT))
        self.blob_output_file.write(bytearray(4194304))
        self.assertEqual(self.blob_output_file.position, 4194304 + len(TEST_CONTENT))

    def test_write_with_invalid_offset(self):
        with self.assertRaises(NotImplementedError):
            self.blob_output_file.seek(1, whence=1)

    def test_seek(self):
        self.blob_input_file.seek(6)
        self.assertEqual(self.blob_input_file.position, 6)
        self.blob_input_file.seek(5, whence=1)
        self.assertEqual(self.blob_input_file.position, 11)

    def test_close_with_destroy_on_close(self):
        self.temporary_blob_file.delete = MagicMock()
        self.temporary_blob_file.close()
        assert self.temporary_blob_file.delete.call_count == 1

    def test_close_with_wb_mode(self):
        with patch(
            "campaignresourcecentre.custom_storages.custom_azure.AzureBlobFile.delete"
        ) as delete_mock, patch(
            "campaignresourcecentre.custom_storages.custom_azure.AzureBlobFile._write_block"
        ) as write_block_mock:
            self.blob_output_file.close()
            self.assertTrue(write_block_mock.called)
            self.assertFalse(delete_mock.called)

    def test_delete_deletes_blob(self):
        self.blob_output_file.delete()
        assert self.blob_output_file.deleted == True
        assert self.blob_output_file.blob_client.delete_blob.call_count == 1


class MockStorage:
    @property
    def client(self):
        return MockClient()


class MockClient:
    def get_blob_client(self, _):
        return MockBlobClient()


class MockBlobClient:
    def get_blob_properties(self):
        return BlobProperties()

    def stage_block(self, block_id, data):
        pass

    def set_http_headers(self, headers):
        pass

    def delete(self):
        pass

    def commit_block_list(self, block_list):
        pass


class AzureBlobUploadHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.handler = AzureBlobUploadHandler()
        self.handler.storage = MockStorage()
        self.field_name = "file"
        self.file_name = "test.txt"
        self.content_type = "text/plain"
        self.content_length = 12
        self.charset = "utf-8"
        self.content_type_extra = None
        self.chunks = [
            TEST_CONTENT[:5],
            TEST_CONTENT[5:],
        ]
        self.handler.new_file(
            self.field_name,
            self.file_name,
            self.content_type,
            self.content_length,
            self.charset,
            self.content_type_extra,
        )

    def test_new_file(self):
        self.assertIsInstance(self.handler.blob_name, str)
        self.assertEqual(self.handler.file_name, self.file_name)
        self.assertIsInstance(self.handler.blob_file, AzureBlobFile)
        self.assertEqual(self.handler.chunks, 0)

    def test_receive_data_chunk(self):
        self.handler.blob_file = MagicMock()

        for chunk in self.chunks:
            self.handler.receive_data_chunk(chunk, 0)

        self.handler.blob_file.write.assert_called_with(TEST_CONTENT[5:])

    def test_file_complete(self):
        for chunk in self.chunks:
            self.handler.receive_data_chunk(chunk, 0)

        result = self.handler.file_complete(len(TEST_CONTENT))

        self.assertIsInstance(result, AzureUploadedFile)
        self.assertEqual(result.content_type, self.content_type)
        self.assertEqual(result.size, len(TEST_CONTENT))
        self.assertEqual(result.charset, self.charset)
        self.assertEqual(result.content_type_extra, self.content_type_extra)
