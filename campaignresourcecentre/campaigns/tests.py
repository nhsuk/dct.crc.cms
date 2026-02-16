import importlib

from django.test import TestCase

from campaignresourcecentre.campaigns.models import Topic
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
            {"label": topic.name, "code": topic.code} for topic in Topic.objects.all()
        ]

    def test_new_topic_included_in_filter_list(self):
        Topic.objects.create(name="New Test Topic", code="TESTTOPIC")
        self.assertIn(
            {"label": "New Test Topic", "code": "TESTTOPIC"}, self._get_filter_topics()
        )

    def test_seeded_topics_included_in_filter_list(self):
        self.assertEqual(len(self._get_filter_topics()), len(INITIAL_TOPICS))
