import importlib
import json

from django.core.exceptions import ValidationError
from django.test import TestCase

from campaignresourcecentre.campaigns.models import (
    CampaignPage,
    Topic,
    count_pages_with_topic,
)
from campaignresourcecentre.core.preparetestdata import PrepareTestData
from campaignresourcecentre.wagtailreacttaxonomy.models import load_campaign_topics

_migration = importlib.import_module(
    "campaignresourcecentre.campaigns.migrations.0034_populate_topics"
)
INITIAL_TOPICS = _migration.INITIAL_TOPICS

TOPIC_TAXONOMY = [
    {"label": "Health Topics", "code": "TOPIC", "type": "vocabulary", "children": []},
]


class MigrationPopulatesTopicsTest(TestCase):
    """The data migration pre-populates the Topic table."""

    def test_initial_topics_are_loaded(self):
        expected_codes = {topic["code"] for topic in INITIAL_TOPICS}
        actual_codes = set(Topic.objects.values_list("code", flat=True))
        self.assertEqual(expected_codes, actual_codes)


class TopicAppearsInTaxonomySelectorTest(TestCase):
    """Adding a Topic makes it available in the taxonomy JSON selector."""

    def test_new_topic_appears_in_taxonomy(self):
        Topic.objects.create(name="New Test Topic", code="TESTTOPIC")
        taxonomy = json.loads(json.dumps(TOPIC_TAXONOMY))
        load_campaign_topics(taxonomy)
        codes = [c["code"] for c in taxonomy[0]["children"]]
        self.assertIn("TESTTOPIC", codes)

    def test_taxonomy_children_have_correct_structure(self):
        taxonomy = json.loads(json.dumps(TOPIC_TAXONOMY))
        load_campaign_topics(taxonomy)
        for child in taxonomy[0]["children"]:
            self.assertEqual(child["type"], "term")
            self.assertEqual(child["children"], [])


class TopicShowInFilterTest(TestCase):
    def test_default_includes_all_topics(self):
        Topic.objects.create(name="Hidden Topic", code="HIDDEN", show_in_filter=False)
        Topic.objects.create(name="Visible Topic", code="VISIBLE", show_in_filter=True)
        taxonomy = json.loads(json.dumps(TOPIC_TAXONOMY))
        load_campaign_topics(taxonomy)
        codes = [c["code"] for c in taxonomy[0]["children"]]
        self.assertIn("HIDDEN", codes)
        self.assertIn("VISIBLE", codes)

    def test_visible_only_excludes_hidden_topics(self):
        Topic.objects.create(name="Hidden Topic", code="HIDDEN", show_in_filter=False)
        Topic.objects.create(name="Visible Topic", code="VISIBLE", show_in_filter=True)
        taxonomy = json.loads(json.dumps(TOPIC_TAXONOMY))
        load_campaign_topics(taxonomy, visible_only=True)
        codes = [c["code"] for c in taxonomy[0]["children"]]
        self.assertNotIn("HIDDEN", codes)
        self.assertIn("VISIBLE", codes)

    def test_visible_only_returns_correct_seeded_count(self):
        # 18 of the 26 seeded topics from migration 0034 have show_in_filter=True
        taxonomy = json.loads(json.dumps(TOPIC_TAXONOMY))
        load_campaign_topics(taxonomy, visible_only=True)
        self.assertEqual(len(taxonomy[0]["children"]), 18)


class TopicValidationTest(TestCase):
    """Topic name and code are required and whitespace-only values are rejected."""

    def test_blank_name_is_rejected(self):
        topic = Topic(name="", code="VALID")
        with self.assertRaises(ValidationError) as ctx:
            topic.full_clean()
        self.assertIn("name", ctx.exception.message_dict)

    def test_blank_code_is_rejected(self):
        topic = Topic(name="Valid", code="")
        with self.assertRaises(ValidationError) as ctx:
            topic.full_clean()
        self.assertIn("code", ctx.exception.message_dict)

    def test_whitespace_only_name_is_rejected(self):
        topic = Topic(name="   ", code="VALID")
        with self.assertRaises(ValidationError) as ctx:
            topic.full_clean()
        self.assertIn("name", ctx.exception.message_dict)

    def test_whitespace_only_code_is_rejected(self):
        topic = Topic(name="Valid", code="   ")
        with self.assertRaises(ValidationError) as ctx:
            topic.full_clean()
        self.assertIn("code", ctx.exception.message_dict)

    def test_valid_topic_passes_clean(self):
        topic = Topic(name="Good Topic", code="GOOD")
        topic.full_clean()

    def test_clean_strips_whitespace(self):
        topic = Topic(name="  Padded  ", code="  PAD  ")
        topic.full_clean()
        self.assertEqual(topic.name, "Padded")
        self.assertEqual(topic.code, "PAD")


class CountPagesWithTopicTest(TestCase):
    """count_pages_with_topic handles both Python and JavaScript JSON formats."""

    def setUp(self):
        test_data = PrepareTestData()
        self.campaign_page = test_data.campaign_page
        self.resource_page = test_data.resource_page

    def test_matches_json_with_spaces(self):
        """Seeded data uses json.dumps (spaces after colons) and is matched."""
        campaigns, resources = count_pages_with_topic("EATING")
        self.assertEqual(campaigns, 1)
        self.assertEqual(resources, 1)

    def test_matches_json_without_spaces(self):
        """JSON without spaces after colons (e.g. from JavaScript) is also matched."""
        CampaignPage.objects.filter(pk=self.campaign_page.pk).update(
            taxonomy_json='[{"code":"EATING","label":"Eating well"}]',
        )
        campaigns, resources = count_pages_with_topic("EATING")
        self.assertEqual(campaigns, 1)
        self.assertEqual(resources, 1)

    def test_returns_zero_when_not_tagged(self):
        campaigns, resources = count_pages_with_topic("NONEXISTENT")
        self.assertEqual(campaigns, 0)
        self.assertEqual(resources, 0)

    def test_does_not_partial_match_code(self):
        """'EAT' must not match a page tagged with 'EATING'."""
        campaigns, resources = count_pages_with_topic("EAT")
        self.assertEqual(campaigns, 0)
        self.assertEqual(resources, 0)
