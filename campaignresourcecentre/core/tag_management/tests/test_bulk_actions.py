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


class ManageTagsBulkActionTestCase(BaseTestCase):
    """Test the ManageTagsBulkAction base class shared functionality."""

    def test_apply_changes_success(self):
        """apply_changes should successfully update pages with changes."""
        action = object.__new__(AddTagsBulkAction)
        action.calculated_changes = [
            {
                "page_id": self.resource_page.id,
                "final_tags": [{"code": "test:tag", "label": "Test"}],
                "had_changes": True,
            }
        ]

        num_modified, num_failed = action.apply_changes(self.user)

        self.assertEqual(num_modified, 1)
        self.assertEqual(num_failed, 0)
        self.resource_page.refresh_from_db()
        self.assertIn("test:tag", self.resource_page.taxonomy_json)

    def test_apply_changes_skips_no_changes(self):
        """apply_changes should skip pages without changes."""
        action = object.__new__(AddTagsBulkAction)
        action.calculated_changes = [
            {
                "page_id": self.resource_page.id,
                "final_tags": [],
                "had_changes": False,
            }
        ]

        num_modified, num_failed = action.apply_changes(self.user)

        self.assertEqual(num_modified, 0)
        self.assertEqual(num_failed, 0)

    def test_apply_changes_handles_errors(self):
        """apply_changes should handle errors and track failed changes."""
        action = object.__new__(AddTagsBulkAction)
        action.calculated_changes = [
            {
                "page_id": 99999,
                "final_tags": [{"code": "test", "label": "Test"}],
                "had_changes": True,
            }
        ]

        num_modified, num_failed = action.apply_changes(self.user)

        self.assertEqual(num_modified, 0)
        self.assertEqual(num_failed, 1)
        self.assertIn("error", action.calculated_changes[0])
        self.assertFalse(action.calculated_changes[0]["had_changes"])

    def test_execute_action_with_instance(self):
        """execute_action should call apply_changes when instance provided."""
        instance = object.__new__(AddTagsBulkAction)
        instance.calculated_changes = [
            {
                "page_id": self.resource_page.id,
                "final_tags": [{"code": "test", "label": "Test"}],
                "had_changes": True,
            }
        ]

        num_modified, num_failed = AddTagsBulkAction.execute_action(
            [self.resource_page],
            bulk_action_instance=instance,
            user=self.user,
        )

        self.assertEqual(num_modified, 1)
        self.assertEqual(num_failed, 0)

    def test_execute_action_without_instance(self):
        """execute_action should fail gracefully without instance."""
        num_modified, num_failed = AddTagsBulkAction.execute_action(
            [self.resource_page],
            user=self.user,
        )

        self.assertEqual(num_modified, 0)
        self.assertEqual(num_failed, 1)

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
            action._save_tags(alias_page, [], self.user)

        self.assertIn("alias", str(context.exception).lower())

    def test_apply_changes_skips_alias_pages(self):
        """apply_changes should skip alias pages with error."""
        alias_page = self.campaign_page.create_alias(update_slug="alias-campaign")
        action = object.__new__(AddTagsBulkAction)
        action.calculated_changes = [
            {
                "page_id": alias_page.id,
                "final_tags": [{"code": "test", "label": "Test"}],
                "had_changes": True,
            }
        ]

        num_modified, num_failed = action.apply_changes(self.user)

        self.assertEqual(num_modified, 0)
        self.assertEqual(num_failed, 1)
        self.assertIn("error", action.calculated_changes[0])
        self.assertIn("alias", action.calculated_changes[0]["error"].lower())
        self.assertFalse(action.calculated_changes[0]["had_changes"])

    def test_save_tags_with_existing_draft_preserves_draft(self):
        """_save_tags on a live page with an existing draft should publish live changes and keep draft as latest, recalculated via calculate_draft_tags."""
        self.resource_page.taxonomy_json = json.dumps([])
        self.resource_page.save_revision().publish()

        draft_only_tags = [{"code": "draft:only", "label": "Draft Only"}]
        self.resource_page.taxonomy_json = json.dumps(draft_only_tags)
        self.resource_page.save_revision(user=self.user)

        action = object.__new__(AddTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "merge",
                "tags_to_add": json.dumps(
                    [{"code": "extra:draft", "label": "Extra Draft"}]
                ),
            },
        )

        live_tags = [{"code": "live:tag", "label": "Live Tag"}]
        action._save_tags(
            self.resource_page, live_tags, self.user, operation_mode="merge"
        )

        self.resource_page.refresh_from_db()
        live_saved = json.loads(self.resource_page.taxonomy_json)
        self.assertEqual(live_saved, live_tags)

        # Verify latest revision remains a draft and contains recalculated draft tags
        latest_rev = self.resource_page.latest_revision
        live_rev = self.resource_page.live_revision
        self.assertIsNotNone(latest_rev)
        self.assertIsNotNone(live_rev)
        self.assertNotEqual(latest_rev.id, live_rev.id)

        latest_obj = latest_rev.as_object()
        latest_draft_tags = json.loads(latest_obj.taxonomy_json)
        # Expected draft tags = original draft_only_tags merged with tags_to_add (no replace)
        expected_draft_tags = draft_only_tags + [
            {"code": "extra:draft", "label": "Extra Draft"}
        ]
        # Order should match merge behavior without duplicates
        self.assertEqual(latest_draft_tags, expected_draft_tags)


class RemoveTagsBulkActionTestCase(BaseTestCase):
    """Test RemoveTagsBulkAction functionality."""

    def test_calculate_changes_removes_tags(self):
        """calculate_changes should correctly remove specified tags."""
        action = object.__new__(RemoveTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "remove",
                "tags_to_remove": json.dumps(
                    {str(self.campaign_page.id): ["health:gp"]}
                ),
            },
        )

        items = [
            {
                "item": self.campaign_page,
                "taxonomy_tags": json.loads(self.campaign_page.taxonomy_json),
            }
        ]

        changes = action.calculate_changes(items)

        self.assertEqual(len(changes), 1)
        self.assertEqual(len(changes[0]["final_tags"]), 1)
        self.assertEqual(changes[0]["final_tags"][0]["code"], "health:hospital")
        self.assertEqual(len(changes[0]["tags_removed"]), 1)
        self.assertTrue(changes[0]["had_changes"])

    def test_removed_tags_are_saved_after_preview(self):
        """Integration test: remove tags through complete flow."""
        instance = object.__new__(RemoveTagsBulkAction)
        original_tags = json.loads(self.campaign_page.taxonomy_json)
        instance.calculated_changes = [
            {
                "page_id": self.campaign_page.id,
                "final_tags": [original_tags[1]],  # Keep only hospital
                "had_changes": True,
            }
        ]

        num_modified, num_failed = RemoveTagsBulkAction.execute_action(
            [self.campaign_page],
            bulk_action_instance=instance,
            user=self.user,
        )

        self.assertEqual(num_modified, 1)
        self.assertEqual(num_failed, 0)
        self.campaign_page.refresh_from_db()
        saved_tags = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(len(saved_tags), 1)
        self.assertEqual(saved_tags[0]["code"], "health:hospital")

    def test_remove_tags_with_existing_draft_preserves_and_updates_draft(self):
        """Removing tags on live page with draft should update live and recalculate draft independently."""
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
        action._save_tags(self.campaign_page, live_tags_after, self.user)

        self.campaign_page.refresh_from_db()
        live_saved = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(len(live_saved), 1)
        self.assertEqual(live_saved[0]["code"], "health:hospital")

        latest_rev = self.campaign_page.latest_revision
        live_rev = self.campaign_page.live_revision
        self.assertNotEqual(latest_rev.id, live_rev.id)

        draft_obj = latest_rev.as_object()
        draft_tags = json.loads(draft_obj.taxonomy_json)
        expected_draft = [
            {"code": "health:hospital", "label": "Hospital"},
            {"code": "health:dental", "label": "Dental"},
        ]
        self.assertEqual(draft_tags, expected_draft)


class AddTagsBulkActionTestCase(BaseTestCase):
    """Test AddTagsBulkAction functionality."""

    def test_calculate_changes_merge_mode(self):
        """calculate_changes should add tags in merge mode."""
        action = object.__new__(AddTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "merge",
                "tags_to_add": json.dumps(
                    [
                        {"code": "health:dental", "label": "Dental"},
                        {"code": "health:mental", "label": "Mental Health"},
                    ]
                ),
            },
        )

        items = [
            {
                "item": self.campaign_page,
                "taxonomy_tags": json.loads(self.campaign_page.taxonomy_json),
            }
        ]

        changes = action.calculate_changes(items)

        self.assertEqual(len(changes), 1)
        self.assertEqual(len(changes[0]["final_tags"]), 4)  # 2 existing + 2 new
        self.assertEqual(len(changes[0]["tags_added"]), 2)
        self.assertTrue(changes[0]["had_changes"])

    def test_calculate_changes_merge_skips_duplicates(self):
        """calculate_changes should skip duplicate tags in merge mode."""
        action = object.__new__(AddTagsBulkAction)

        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "merge",
                "tags_to_add": json.dumps([{"code": "health:gp", "label": "GP"}]),
            },
        )

        items = [
            {
                "item": self.campaign_page,
                "taxonomy_tags": json.loads(self.campaign_page.taxonomy_json),
            }
        ]

        changes = action.calculate_changes(items)

        self.assertEqual(len(changes[0]["tags_added"]), 0)
        self.assertFalse(changes[0]["had_changes"])

    def test_calculate_changes_replace_mode(self):
        """calculate_changes should replace all tags in replace mode."""
        action = object.__new__(AddTagsBulkAction)
        action.request = self._create_mock_request(
            method="POST",
            data={
                "tag_operation_mode": "replace",
                "tags_to_add": json.dumps(
                    [
                        {"code": "health:dental", "label": "Dental"},
                        {"code": "health:vision", "label": "Vision"},
                    ]
                ),
            },
        )

        items = [
            {
                "item": self.campaign_page,
                "taxonomy_tags": json.loads(self.campaign_page.taxonomy_json),
            }
        ]

        changes = action.calculate_changes(items)

        self.assertEqual(len(changes[0]["final_tags"]), 2)
        self.assertEqual(len(changes[0]["tags_added"]), 2)
        self.assertEqual(
            len(changes[0]["tags_removed"]), 2
        )  # Removes both existing tags
        self.assertTrue(changes[0]["had_changes"])

    def test_integration_add_tags_end_to_end(self):
        """Integration test: add tags through complete flow."""
        instance = object.__new__(AddTagsBulkAction)
        tags_to_add = [{"code": "health:gp", "label": "GP"}]
        instance.calculated_changes = [
            {
                "page_id": self.resource_page.id,
                "final_tags": tags_to_add,
                "had_changes": True,
            }
        ]

        num_modified, num_failed = AddTagsBulkAction.execute_action(
            [self.resource_page],
            bulk_action_instance=instance,
            user=self.user,
        )

        self.assertEqual(num_modified, 1)
        self.assertEqual(num_failed, 0)
        self.resource_page.refresh_from_db()
        saved_tags = json.loads(self.resource_page.taxonomy_json)
        self.assertEqual(len(saved_tags), 1)
        self.assertEqual(saved_tags[0]["code"], "health:gp")
        self.resource_page.refresh_from_db()
        saved_tags = json.loads(self.resource_page.taxonomy_json)
        self.assertEqual(len(saved_tags), 1)
        self.assertEqual(saved_tags[0]["code"], "health:gp")

    def test_add_tags_with_draft_merge_mode_preserves_and_merges_draft(self):
        """Adding tags to live page with draft in merge mode should update live and merge into draft."""
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
        action._save_tags(
            self.campaign_page, live_tags, self.user, operation_mode="merge"
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
        action._save_tags(
            self.campaign_page, live_tags, self.user, operation_mode="replace"
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
