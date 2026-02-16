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


class MigrationPopulatesTopicsTest(TestCase):
    """The data migration pre-populates the Topic table."""

    def test_initial_topics_are_loaded(self):
        expected_codes = {topic["code"] for topic in INITIAL_TOPICS}
        actual_codes = set(Topic.objects.values_list("code", flat=True))
        self.assertEqual(expected_codes, actual_codes)


class TopicAppearsInTaxonomySelectorTest(TestCase):
    """Adding a Topic makes it available in the taxonomy JSON selector."""

    def _load_taxonomy_with_topics(self):
        taxonomy_data = [
            {
                "label": "Health Topics",
                "code": "TOPIC",
                "type": "vocabulary",
                "children": [],
            },
        ]
        load_campaign_topics(taxonomy_data)
        return taxonomy_data[0]["children"]

    def test_new_topic_appears_in_taxonomy(self):
        Topic.objects.create(name="New Test Topic", code="TESTTOPIC")
        children = self._load_taxonomy_with_topics()
        codes = [child["code"] for child in children]
        self.assertIn("TESTTOPIC", codes)

    def test_taxonomy_children_have_correct_structure(self):
        children = self._load_taxonomy_with_topics()
        for child in children:
            self.assertEqual(child["type"], "term")
            self.assertEqual(child["children"], [])


class TopicAppearsAsCampaignFilterTest(TestCase):
    """Adding a Topic makes it appear as a filter option on the main Campaigns page."""

    def _get_filter_topics(self):
        return [
            {"label": topic.name, "code": topic.code}
            for topic in Topic.objects.filter(show_in_filter=True)
        ]

    def test_new_topic_included_in_filter_list(self):
        Topic.objects.create(name="New Test Topic", code="TESTTOPIC")
        self.assertIn(
            {"label": "New Test Topic", "code": "TESTTOPIC"}, self._get_filter_topics()
        )

    def test_topic_hidden_from_filter_when_show_in_filter_is_false(self):
        Topic.objects.create(name="Hidden Topic", code="HIDDEN", show_in_filter=False)
        codes = [topic["code"] for topic in self._get_filter_topics()]
        self.assertNotIn("HIDDEN", codes)

    def test_seeded_topics_included_in_filter_list(self):
        # 18 topics from migration 0034 have show_in_filter=True (8 legacy ones are hidden)
        self.assertEqual(len(self._get_filter_topics()), 18)


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
            ]
        )
        self.campaign_page.taxonomy_json = taxonomy_json
        self.campaign_page.save(update_fields=["taxonomy_json"])
        self.resource_page.taxonomy_json = taxonomy_json
        self.resource_page.save(update_fields=["taxonomy_json"])

    def test_deleting_topic_removes_tag_from_campaign_page(self):
        self.topic.delete()
        self.campaign_page.refresh_from_db()
        codes = [item["code"] for item in json.loads(self.campaign_page.taxonomy_json)]
        self.assertNotIn("TESTTOPIC", codes)
        self.assertIn("MENTALHEALTH", codes)

    def test_deleting_topic_removes_tag_from_resource_page(self):
        self.topic.delete()
        self.resource_page.refresh_from_db()
        codes = [item["code"] for item in json.loads(self.resource_page.taxonomy_json)]
        self.assertNotIn("TESTTOPIC", codes)
        self.assertIn("MENTALHEALTH", codes)
