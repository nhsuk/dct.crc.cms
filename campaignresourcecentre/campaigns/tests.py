import importlib
import json

from django.test import TestCase

from campaignresourcecentre.campaigns.models import Topic
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


class TopicDeletionRemovesTagsTest(TestCase):
    """Deleting a Topic removes its tag from every campaign and resource page."""

    def setUp(self):
        test_data = PrepareTestData()
        self.campaign_page = test_data.campaign_page
        self.resource_page = test_data.resource_page

        self.topic = Topic.objects.create(name="Test Topic", code="TESTTOPIC")

        taxonomy_json = json.dumps(
            [
                {"code": "TESTTOPIC", "label": "Test Topic"},
                {"code": "MENTALHEALTH", "label": "Mental health"},
            ],
        )
        self.campaign_page.taxonomy_json = taxonomy_json
        self.campaign_page.save(update_fields=["taxonomy_json"])
        self.resource_page.taxonomy_json = taxonomy_json
        self.resource_page.save(update_fields=["taxonomy_json"])

    def test_deleting_topic_removes_tag_from_campaign_page(self):
        self.topic.delete()
        self.campaign_page.refresh_from_db()
        tags = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(tags, [{"code": "MENTALHEALTH", "label": "Mental health"}])

    def test_deleting_topic_removes_tag_from_resource_page(self):
        self.topic.delete()
        self.resource_page.refresh_from_db()
        tags = json.loads(self.resource_page.taxonomy_json)
        self.assertEqual(tags, [{"code": "MENTALHEALTH", "label": "Mental health"}])

    def test_deleting_topic_creates_revision_on_campaign_page(self):
        revisions_before = self.campaign_page.revisions.count()
        self.topic.delete()
        revisions_after = self.campaign_page.revisions.count()
        self.assertGreater(revisions_after, revisions_before)

    def test_deleting_topic_creates_revision_on_resource_page(self):
        revisions_before = self.resource_page.revisions.count()
        self.topic.delete()
        revisions_after = self.resource_page.revisions.count()
        self.assertGreater(revisions_after, revisions_before)
