from django.test import SimpleTestCase, TestCase
from unittest.mock import patch, MagicMock
from campaignresourcecentre.resources.models import ResourceItem
from campaignresourcecentre.core.templatetags.get_db_fields import get_field


class GetFieldTagTest(TestCase):
    def setUp(self):
        self.mock_resource_item = MagicMock(spec=ResourceItem)
        self.mock_resource_item.sku = "sku123"

    def test_get_field_returns_resource_item(self):
        sku = "sku123"
        mock_queryset = MagicMock(spec=ResourceItem.objects)
        mock_queryset.first.return_value = self.mock_resource_item
        with patch.object(ResourceItem.objects, "filter", return_value=mock_queryset):
            result = get_field(sku)
        self.assertEqual(result, self.mock_resource_item)

    def test_get_field_invalid_sku_returns_empty_resource(self):
        invalid_skus = ["", "sku123", None]

        for sku in invalid_skus:
            result = get_field(sku)
            self.assertEqual(result.title, "Item not found")
