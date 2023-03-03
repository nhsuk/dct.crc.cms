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

    def test_get_field_raises_does_not_exist_when_sku_missing(self):
        sku = ""
        with self.assertRaises(ResourceItem.DoesNotExist):
            get_field(sku)

    def test_get_field_raises_does_not_exist_when_sku_unmatched(self):
        sku = "sku123"
        mock_queryset = MagicMock(spec=ResourceItem.objects)
        mock_queryset.first.return_value = None
        mock_queryset.first.side_effect = ResourceItem.DoesNotExist
        with patch.object(ResourceItem.objects, "filter", return_value=mock_queryset):
            with self.assertRaises(ResourceItem.DoesNotExist):
                get_field(sku)
