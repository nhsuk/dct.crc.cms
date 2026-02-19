import json
from django.test import TestCase
from django.core.exceptions import ValidationError

from campaignresourcecentre.core.preparetestdata import PrepareTestData
from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage


class TaxonomyMixinValidationTestCase(TestCase):
    """Test TaxonomyMixin validation for topic tag requirements."""

    @classmethod
    def setUpTestData(cls):
        td = PrepareTestData()
        cls.campaign_page = td.campaign_page
        cls.resource_page = td.resource_page

    def test_clean_requires_at_least_one_topic_tag(self):
        """clean() should raise ValidationError when no TOPIC tags are present."""
        self.campaign_page.refresh_from_db()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "ADULTS", "label": "Adults"},
                {"code": "HEALTHPROFS", "label": "Healthcare professionals"},
            ]
        )

        with self.assertRaises(ValidationError) as context:
            self.campaign_page.clean()

        self.assertIn("select at least one topic tag", str(context.exception).lower())

    def test_clean_passes_with_topic_tag(self):
        """clean() should pass when at least one TOPIC tag is present."""
        self.campaign_page.refresh_from_db()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "ADULTS", "label": "Adults"},
            ]
        )

        self.campaign_page.clean()

    def test_clean_passes_with_multiple_topic_tags(self):
        """clean() should pass when multiple TOPIC tags are present."""
        self.resource_page.refresh_from_db()

        self.resource_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "COVID", "label": "Coronavirus"},
                {"code": "DENTAL", "label": "Dental health"},
                {"code": "ADULTS", "label": "Adults"},
            ]
        )

        self.resource_page.clean()

    def test_clean_fails_with_empty_taxonomy_json(self):
        """clean() should fail when taxonomy_json is empty."""
        self.campaign_page.refresh_from_db()

        self.campaign_page.taxonomy_json = json.dumps([])

        with self.assertRaises(ValidationError) as context:
            self.campaign_page.clean()

        self.assertIn("select at least one topic tag", str(context.exception).lower())

    def test_clean_fails_with_null_taxonomy_json(self):
        """clean() should fail when taxonomy_json is null."""
        self.campaign_page.refresh_from_db()

        self.campaign_page.taxonomy_json = None

        with self.assertRaises(ValidationError) as context:
            self.campaign_page.clean()

        self.assertIn("select at least one topic tag", str(context.exception).lower())

    def test_clean_passes_with_topic_and_other_vocabularies(self):
        """clean() should pass when TOPIC tag is present along with other vocabulary tags."""
        self.campaign_page.refresh_from_db()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "ADULTS", "label": "Adults"},
                {"code": "LONDON", "label": "London"},
                {"code": "ARABIC", "label": "Arabic"},
            ]
        )

        self.campaign_page.clean()

    def test_clean_validates_topic_vocabulary_exists(self):
        """clean() should raise ValidationError if TOPIC vocabulary is missing from taxonomy."""
        from campaignresourcecentre.wagtailreacttaxonomy.models import TaxonomyTerms

        current_taxonomy = TaxonomyTerms.objects.get(taxonomy_id="crc_taxonomy")
        original_terms = current_taxonomy.terms_json

        try:
            current_taxonomy.terms_json = json.dumps(
                [
                    {
                        "label": "Target Audience",
                        "code": "TARGAUD",
                        "type": "vocabulary",
                        "children": [
                            {
                                "label": "Adults",
                                "code": "ADULTS",
                                "type": "term",
                                "children": [],
                            }
                        ],
                    }
                ]
            )
            current_taxonomy.save()

            self.campaign_page.refresh_from_db()
            self.campaign_page.taxonomy_json = json.dumps(
                [{"code": "ADULTS", "label": "Adults"}]
            )

            with self.assertRaises(ValidationError) as context:
                self.campaign_page.clean()

            self.assertIn("topic vocabulary", str(context.exception).lower())
        finally:
            current_taxonomy.terms_json = original_terms
            current_taxonomy.save()

    def test_taxonomy_property_returns_parsed_json(self):
        """taxonomy property should return parsed list from taxonomy_json."""
        self.campaign_page.refresh_from_db()

        taxonomy_data = [
            {"code": "CANCER", "label": "Cancer"},
            {"code": "ADULTS", "label": "Adults"},
        ]
        self.campaign_page.taxonomy_json = json.dumps(taxonomy_data)

        result = self.campaign_page.taxonomy

        self.assertEqual(result, taxonomy_data)
        self.assertIsInstance(result, list)

    def test_taxonomy_property_returns_empty_list_when_null(self):
        """taxonomy property should return empty list when taxonomy_json is null."""
        self.campaign_page.refresh_from_db()
        self.campaign_page.taxonomy_json = None

        result = self.campaign_page.taxonomy

        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
