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

    def test_save_tags_updates_taxonomy_json(self):
        """_save_tags should update page's taxonomy_json field."""
        action = object.__new__(AddTagsBulkAction)
        new_tags = [{"code": "new:tag", "label": "New Tag"}]

        action._save_tags(self.resource_page, new_tags, self.user)

        self.resource_page.refresh_from_db()
        self.assertEqual(json.loads(self.resource_page.taxonomy_json), new_tags)

    def test_save_tags_creates_revision(self):
        """_save_tags should create a revision."""
        action = object.__new__(AddTagsBulkAction)
        new_tags = [{"code": "new:tag", "label": "New Tag"}]

        initial_revisions = self.resource_page.revisions.count()
        action._save_tags(self.resource_page, new_tags, self.user)

        self.assertEqual(self.resource_page.revisions.count(), initial_revisions + 1)

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
