import json
from unittest.mock import patch, Mock
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from campaignresourcecentre.core.tag_management.bulk_actions import (
    RemoveTagsBulkAction,
    AddTagsBulkAction,
)
from campaignresourcecentre.core.preparetestdata import PrepareTestData


User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        td = PrepareTestData()
        cls.campaign_page = td.campaign_page
        cls.campaign_hub_page = td.campaign_hub_page
        cls.resource_page = td.resource_page
        cls.user = User.objects.get(username="wagtail")

        # Set taxonomy_json on test pages for testing
        cls.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "health:gp", "label": "GP"},
                {"code": "health:hospital", "label": "Hospital"},
            ]
        )
        cls.campaign_page.save_revision().publish()

        cls.resource_page.taxonomy_json = json.dumps([])
        cls.resource_page.save_revision().publish()

    def setUp(self):
        self.factory = RequestFactory()

    def _create_mock_request(self, method="GET", data=None, user=None):
        if method == "POST":
            post_data = data or {}
            post_data["next"] = "/"
            request = self.factory.post("/", data=post_data)
        else:
            request = self.factory.get("/", {"next": "/"})
        request.user = user or self.user
        return request


class BaseTagBulkActionTestCase(BaseTestCase):
    """Test the BaseTagBulkAction base class shared functionality."""

    def test_check_perm_excludes_alias_pages(self):
        """check_perm should return False for alias pages."""
        action = object.__new__(AddTagsBulkAction)
        alias_page = self.campaign_page.create_alias(update_slug="alias-campaign")

        self.assertFalse(action.check_perm(alias_page))
        self.assertTrue(action.check_perm(self.campaign_page))

    def test_save_tags_raises_error_for_alias(self):
        """_save_tags should raise ValueError for alias pages."""
        action = object.__new__(AddTagsBulkAction)
        alias_page = self.campaign_page.create_alias(update_slug="alias-campaign")

        with self.assertRaises(ValueError) as context:
            action._save_tags(alias_page, [], None, self.user)

        self.assertIn("alias", str(context.exception).lower())


class RemoveTagsBulkActionTestCase(BaseTestCase):
    """Test RemoveTagsBulkAction functionality."""

    def test_remove_tags_with_existing_draft_preserves_and_updates_draft(self):
        """Removing tags on live page with draft should update live and recalculate draft independently."""
        self.campaign_page.refresh_from_db()
        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "health:gp", "label": "GP"},
                {"code": "health:hospital", "label": "Hospital"},
            ]
        )
        self.campaign_page.save_revision().publish()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "health:gp", "label": "GP"},
                {"code": "health:hospital", "label": "Hospital"},
                {"code": "health:dental", "label": "Dental"},
            ]
        )
        self.campaign_page.save_revision(user=self.user)  # Draft only

        action = object.__new__(RemoveTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tags_to_remove": json.dumps(
                    {str(self.campaign_page.id): ["health:gp"]}
                ),
            },
        )
        action.action_type = "remove_tags"

        live_tags_after = [{"code": "health:hospital", "label": "Hospital"}]
        draft_tags_after = [
            {"code": "health:hospital", "label": "Hospital"},
            {"code": "health:dental", "label": "Dental"},
        ]
        action._save_tags(
            self.campaign_page, live_tags_after, draft_tags_after, self.user
        )

        self.campaign_page.refresh_from_db()
        live_saved = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(len(live_saved), 1)
        self.assertEqual(live_saved[0]["code"], "health:hospital")

        latest_rev = self.campaign_page.latest_revision
        live_rev = self.campaign_page.live_revision
        self.assertNotEqual(latest_rev.id, live_rev.id)

        draft_obj = latest_rev.as_object()
        draft_tags = json.loads(draft_obj.taxonomy_json)
        self.assertEqual(draft_tags, draft_tags_after)


class AddTagsBulkActionTestCase(BaseTestCase):
    """Test AddTagsBulkAction functionality."""

    def test_add_tags_with_draft_merge_mode_preserves_and_merges_draft(self):
        """Adding tags to live page with draft in merge mode should update live and merge into draft."""
        self.campaign_page.refresh_from_db()
        self.campaign_page.taxonomy_json = json.dumps(
            [{"code": "health:gp", "label": "GP"}]
        )
        self.campaign_page.save_revision().publish()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "health:gp", "label": "GP"},
                {"code": "health:dental", "label": "Dental"},
            ]
        )
        self.campaign_page.save_revision(user=self.user)

        action = object.__new__(AddTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "merge",
                "tags_to_add": json.dumps(
                    [{"code": "health:vision", "label": "Vision"}]
                ),
            },
        )
        action.action_type = "add_tags"

        live_tags = [
            {"code": "health:gp", "label": "GP"},
            {"code": "health:vision", "label": "Vision"},
        ]
        draft_tags = [
            {"code": "health:gp", "label": "GP"},
            {"code": "health:dental", "label": "Dental"},
            {"code": "health:vision", "label": "Vision"},
        ]
        action._save_tags(
            self.campaign_page, live_tags, draft_tags, self.user
        )

        self.campaign_page.refresh_from_db()
        live_saved = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(len(live_saved), 2)
        codes = {tag["code"] for tag in live_saved}
        self.assertEqual(codes, {"health:gp", "health:vision"})

        latest_rev = self.campaign_page.latest_revision
        live_rev = self.campaign_page.live_revision
        self.assertNotEqual(latest_rev.id, live_rev.id)

        draft_obj = latest_rev.as_object()
        draft_tags = json.loads(draft_obj.taxonomy_json)
        self.assertEqual(len(draft_tags), 3)
        draft_codes = {tag["code"] for tag in draft_tags}
        self.assertEqual(draft_codes, {"health:gp", "health:dental", "health:vision"})

    def test_add_tags_with_draft_replace_mode_replaces_draft(self):
        """Adding tags to live page with draft in replace mode should update live and replace draft tags."""
        self.campaign_page.refresh_from_db()
        self.campaign_page.taxonomy_json = json.dumps(
            [{"code": "health:gp", "label": "GP"}]
        )
        self.campaign_page.save_revision().publish()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "health:gp", "label": "GP"},
                {"code": "health:dental", "label": "Dental"},
            ]
        )
        self.campaign_page.save_revision(user=self.user)

        action = object.__new__(AddTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "replace",
                "tags_to_add": json.dumps(
                    [{"code": "health:vision", "label": "Vision"}]
                ),
            },
        )
        action.action_type = "add_tags"

        live_tags = [{"code": "health:vision", "label": "Vision"}]
        draft_tags = [{"code": "health:vision", "label": "Vision"}]
        action._save_tags(
            self.campaign_page,
            live_tags,
            draft_tags,
            self.user
        )

        self.campaign_page.refresh_from_db()
        live_saved = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(len(live_saved), 1)
        self.assertEqual(live_saved[0]["code"], "health:vision")

        latest_rev = self.campaign_page.latest_revision
        live_rev = self.campaign_page.live_revision
        self.assertNotEqual(latest_rev.id, live_rev.id)

        draft_obj = latest_rev.as_object()
        draft_tags = json.loads(draft_obj.taxonomy_json)
        self.assertEqual(len(draft_tags), 1)
        self.assertEqual(draft_tags[0]["code"], "health:vision")
