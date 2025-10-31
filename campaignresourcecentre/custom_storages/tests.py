import unittest
from unittest.mock import MagicMock, patch

from azure.storage.blob import BlobProperties
from campaignresourcecentre.custom_storages.custom_azure_uploader import (
    AzureBlobUploadHandler,
    AzureUploadedFile,
)
from campaignresourcecentre.custom_storages.custom_azure_file import (
    AzureBlobStorageFile,
)
from campaignresourcecentre.custom_storages.custom_azure_storage import (
    AzureMediaStorage,
    SearchStorage,
)
from django.core.files.storage import default_storage


TEST_CONTENT = b"test_content"


class TestAzureBlobFile(unittest.TestCase):
    def setUp(self):
        self.storage = MagicMock()
        self.container_client = MagicMock()
        self.blob_client = MagicMock()
        self.container_client.get_blob_client.return_value = self.blob_client
        self.storage.client = self.container_client
        self.blob_input_file = AzureBlobStorageFile(
            "test_blob_in", self.storage, mode="rb"
        )
        self.blob_output_file = AzureBlobStorageFile(
            "test_blob_out", self.storage, mode="wb"
        )
        self.temporary_blob_file = AzureBlobStorageFile(
            "test_blob_in", self.storage, mode="rb"
        )

    def test_init(self):
        self.assertEqual(self.blob_input_file.blob_name, "test_blob_in")
        self.assertEqual(self.blob_input_file.mode, "rb")
        self.assertEqual(self.blob_input_file.block_size, 4194304)
        self.assertEqual(self.blob_input_file.container_client, self.container_client)
        self.assertEqual(self.blob_input_file.blob_client, self.blob_client)
        self.assertEqual(self.blob_input_file.position, 0)
        self.assertFalse(self.blob_input_file.reported_closed)
        self.assertEqual(self.blob_output_file.blob_name, "test_blob_out")
        self.assertEqual(self.blob_output_file.mode, "wb")
        self.assertEqual(self.blob_output_file.block_size, 4194304)
        self.assertEqual(self.blob_output_file.container_client, self.container_client)
        self.assertEqual(self.blob_output_file.blob_client, self.blob_client)
        self.assertEqual(self.blob_output_file.position, 0)
        self.assertFalse(self.blob_output_file.reported_closed)

    def test_init_with_wb_mode(self):
        self.assertEqual(self.blob_output_file.block_buffer, bytearray(4194304))
        self.assertEqual(self.blob_output_file.block_offset, 0)
        self.assertEqual(self.blob_output_file.block_list, [])
        self.assertEqual(self.blob_output_file.size, 0)

    def test_init_with_invalid_mode(self):
        with self.assertRaises(NotImplementedError):
            AzureBlobStorageFile("test_blob", self.storage, mode="invalid")

    def test_write(self):
        self.blob_output_file.write(TEST_CONTENT)
        self.assertEqual(self.blob_output_file.position, len(TEST_CONTENT))
        self.blob_output_file.write(bytearray(4194304))
        self.assertEqual(self.blob_output_file.position, 4194304 + len(TEST_CONTENT))

    def test_close_with_wb_mode(self):
        with patch(
            "campaignresourcecentre.custom_storages.custom_azure_file.AzureBlobStorageFile.delete"
        ) as delete_mock, patch(
            "campaignresourcecentre.custom_storages.custom_azure_file.AzureBlobStorageFile._write_block"
        ) as write_block_mock:
            self.blob_output_file.close()
            self.assertTrue(write_block_mock.called)
            self.assertFalse(delete_mock.called)

    def test_delete_deletes_blob(self):
        self.blob_output_file.delete()
        assert self.blob_output_file.blob_client.delete_blob.call_count == 1


class MockStorage:
    @property
    def client(self):
        return MockClient()

    def get_available_name(self, name):
        return name

    def get_valid_name(self, name):
        return default_storage.get_valid_name(name)


class MockClient:
    def get_blob_client(self, _):
        return MockBlobClient()


class MockBlobClient:
    def get_blob_properties(self):
        return BlobProperties()

    def stage_block(self, block_id, data):
        # Omitted for mocking
        pass

    def set_http_headers(self, headers):
        # Omitted for mocking
        pass

    def delete(self):
        # Omitted for mocking
        pass

    @property
    def url(self):
        return "test_blob_url"

    def commit_block_list(self, block_list):
        # Omitted for mocking
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
        self.assertIsInstance(self.handler.blob_file, AzureBlobStorageFile)
        self.assertEqual(self.handler.chunks, 0)

    def test_file_name_with_special_characters_are_cleaned(self):
        invalid_file_names = [
            {"name": "file with spaces.txt", "expected": "file_with_spaces.txt"},
            {"name": "file:with:colons.pdf", "expected": "filewithcolons.pdf"},
            {"name": "file*with*asterisks.jpg", "expected": "filewithasterisks.jpg"},
            {"name": "file?with?questions.png", "expected": "filewithquestions.png"},
            {"name": "file<with>brackets.xls", "expected": "filewithbrackets.xls"},
            {"name": 'file"with"quotes.csv', "expected": "filewithquotes.csv"},
            {"name": "file|with|pipes.zip", "expected": "filewithpipes.zip"},
            {"name": "file@with@at.mp3", "expected": "filewithat.mp3"},
            {"name": "file#with#hash.mp4", "expected": "filewithhash.mp4"},
            {"name": "file%with%percent.docx", "expected": "filewithpercent.docx"},
            {"name": "file^with^caret.pptx", "expected": "filewithcaret.pptx"},
            {"name": "file&with&ersand.odt", "expected": "filewithersand.odt"},
            {"name": "file+with+plus.ods", "expected": "filewithplus.ods"},
            {"name": "file=with=equals.odp", "expected": "filewithequals.odp"},
            {
                "name": "file[with]square_brackets.txt",
                "expected": "filewithsquare_brackets.txt",
            },
            {
                "name": "file{with}curly_braces.doc",
                "expected": "filewithcurly_braces.doc",
            },
            {
                "name": "file(with)parentheses.pdf",
                "expected": "filewithparentheses.pdf",
            },
            {"name": "file~with~tilde.jpg", "expected": "filewithtilde.jpg"},
            {"name": "file`with`backticks.png", "expected": "filewithbackticks.png"},
            {
                "name": "file!with!exclamation.xls",
                "expected": "filewithexclamation.xls",
            },
            {"name": "file$with$dollar.csv", "expected": "filewithdollar.csv"},
            {
                "name": "file_with_backslash\\.zip",
                "expected": "file_with_backslash.zip",
            },
            {"name": "file_with_§_section.mp3", "expected": "file_with__section.mp3"},
            {"name": "file_with_¶_pilcrow.mp4", "expected": "file_with__pilcrow.mp4"},
            {
                "name": "file_with_©_copyright.docx",
                "expected": "file_with__copyright.docx",
            },
            {
                "name": "file_with_®_registered.pptx",
                "expected": "file_with__registered.pptx",
            },
            {
                "name": "file_with_™_trademark.odt",
                "expected": "file_with__trademark.odt",
            },
        ]

        for invalid_file_name in invalid_file_names:
            file_name = invalid_file_name["name"]
            expected_file_name = invalid_file_name["expected"]
            self.handler.new_file(
                self.field_name,
                file_name,
                self.content_type,
                self.content_length,
                self.charset,
                self.content_type_extra,
            )
            print(f"Testing file name: {file_name}")
            self.assertEqual(self.handler.file_name, expected_file_name)

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


class AzureMediaStorageTestCase(unittest.TestCase):
    def __init__(self, method_name: str = "runTest"):
        super().__init__(method_name)
        self.storage_class_to_mock = "campaignresourcecentre.custom_storages.custom_azure_storage.AzureMediaStorage"
        self.storage_mock_method_names = [
            "get_available_name",
            "exists",
            "_save",
            "_move_temp_blob",
        ]

    def setUp(self):
        self.storage = AzureMediaStorage()
        self.patches = {}
        self.mocks = {}
        for method in self.storage_mock_method_names:
            self.patches[method] = patch(f"{self.storage_class_to_mock}.{method}")
            self.mocks[method] = self.patches[method].start()

    def tearDown(self):
        for patch in self.patches.values():
            patch.stop()

    def test_save_document_when_no_temp_blob_exists_uses_basic_save(self):
        name = "documents/smallfile.pdf"
        self.mocks["get_available_name"].return_value = name
        self.mocks["exists"].return_value = False

        self.storage.save(name, TEST_CONTENT)

        self.assertTrue(self.mocks["_save"].called)

    def test_save_document_when_temp_blob_exists_uses_move_temp_blob(self):
        name = "documents/largefile.pdf"
        self.mocks["get_available_name"].return_value = name
        self.mocks["exists"].return_value = True

        self.storage.save(name, TEST_CONTENT)

        self.assertTrue(self.mocks["_move_temp_blob"].called)

    def test_save_image_rendition_uses_basic_save(self):
        name = "images/rendition.width-200.jpg"
        self.mocks["get_available_name"].return_value = name

        self.storage.save(name, TEST_CONTENT)

        self.assertTrue(self.mocks["_save"].called)

    def test_save_original_image_uses_basic_save(self):
        name = "original_images/original.jpg"
        self.mocks["get_available_name"].return_value = name

        self.storage.save(name, TEST_CONTENT)

        self.assertTrue(self.mocks["_save"].called)


class SearchStorageTestCase(unittest.TestCase):
    def setUp(self):
        self.patches = {}
        self.mocks = {}
        self.patches["storages"] = patch(
            "campaignresourcecentre.custom_storages.custom_azure_storage.storages"
        )
        self.mocks["storages"] = self.patches["storages"].start()
        self.mock_backend = MagicMock()
        self.mocks["storages"].__getitem__.return_value = self.mock_backend

    def tearDown(self):
        for patch in self.patches.values():
            patch.stop()

    def test_search_storage_setup_uses_search_alias(self):
        storage = SearchStorage()
        storage._setup()

        self.mocks["storages"].__getitem__.assert_called_with("search")
        self.assertEqual(storage._wrapped, self.mock_backend)

    def test_search_storage_setup_uses_custom_alias_from_settings(self):
        self.patches["settings"] = patch(
            "campaignresourcecentre.custom_storages.custom_azure_storage.settings"
        )
        self.mocks["settings"] = self.patches["settings"].start()
        self.mocks["settings"].SEARCH_STORAGE_ALIAS = "custom_search"

        storage = SearchStorage()
        storage._setup()

        self.mocks["storages"].__getitem__.assert_called_with("custom_search")
        self.assertEqual(storage._wrapped, self.mock_backend)
