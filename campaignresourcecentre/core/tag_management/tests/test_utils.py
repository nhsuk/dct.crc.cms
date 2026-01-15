import json
from django.test import TestCase
from unittest.mock import Mock

from campaignresourcecentre.core.tag_management.utils import get_page_taxonomy_tags


class GetPageTaxonomyTagsTestCase(TestCase):
    """Test the get_page_taxonomy_tags utility function."""

    def test_returns_empty_list_for_no_taxonomy_data(self):
        """Should return empty list when page has no taxonomy data."""
        page = Mock(spec=[])
        result = get_page_taxonomy_tags(page)
        self.assertEqual(result, [])

    def test_parses_taxonomy_json_field(self):
        """Should parse and return tags from taxonomy_json field."""
        tags = [
            {"code": "tag1", "label": "Tag One"},
            {"code": "tag2", "label": "Tag Two"}
        ]
        page = Mock()
        page.taxonomy_json = json.dumps(tags)
        
        result = get_page_taxonomy_tags(page)
        self.assertEqual(result, tags)

    def test_handles_invalid_json_gracefully(self):
        """Should return empty list for invalid JSON."""
        page = Mock()
        page.taxonomy_json = "invalid json {"
        
        result = get_page_taxonomy_tags(page)
        self.assertEqual(result, [])

    def test_falls_back_to_taxonomy_field(self):
        """Should fall back to taxonomy field if taxonomy_json is None."""
        tags = [
            {"code": "tag1", "label": "Tag One"},
            {"code": "tag2", "label": "Tag Two"}
        ]
        page = Mock()
        page.taxonomy_json = None
        page.taxonomy = tags
        
        result = get_page_taxonomy_tags(page)
        self.assertEqual(result, tags)

    def test_handles_missing_code_or_label(self):
        """Should handle tags with missing code or label fields."""
        tags = [
            {"code": "tag1"},
            {"label": "Tag Two"},
            {}
        ]
        page = Mock()
        page.taxonomy_json = json.dumps(tags)
        
        result = get_page_taxonomy_tags(page)
        self.assertEqual(result, [
            {"code": "tag1", "label": ""},
            {"code": "", "label": "Tag Two"},
            {"code": "", "label": ""}
        ])

    def test_handles_non_list_data(self):
        """Should return empty list for non-list taxonomy data."""
        page = Mock()
        page.taxonomy_json = json.dumps({"not": "a list"})
        
        result = get_page_taxonomy_tags(page)
        self.assertEqual(result, [])
