import json
from unittest.mock import patch
from django.contrib.auth import get_user_model
from wagtail.test.utils import WagtailPageTests

from campaignresourcecentre.core.tag_management.bulk_actions import ManageTagsBulkAction
from campaignresourcecentre.campaigns.models import CampaignPage, CampaignHubPage
from campaignresourcecentre.resources.models import ResourcePage
from campaignresourcecentre.home.models import HomePage


User = get_user_model()


class ManageTagsBulkActionTestCase(WagtailPageTests):
    """Test the ManageTagsBulkAction custom business logic."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for the entire test class."""
        root = HomePage.objects.first()
        if not root:
            root = HomePage.objects.create(
                title="Home",
                slug="home",
                path="00010001",
                depth=2
            )
        
        cls.user = User.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test image for campaign pages
        from wagtail.images.tests.utils import get_test_image_file
        from wagtail.images import get_image_model
        Image = get_image_model()
        cls.test_image = Image.objects.create(
            title="Test image",
            file=get_test_image_file()
        )
        
        # Create a CampaignHubPage as parent (required for search_indexable)
        cls.campaign_hub = CampaignHubPage(
            title="Campaigns",
            slug="campaigns",
            introduction="Campaign Hub"
        )
        root.add_child(instance=cls.campaign_hub)
        
        cls.campaign_page_1 = CampaignPage(
            title="Campaign 1",
            slug="campaign-1",
            description="<p>Test description</p>",
            summary="<p>Test summary</p>",
            image=cls.test_image,
            taxonomy_json='[{"code": "health:gp", "label": "GP"}, {"code": "health:hospital", "label": "Hospital"}]'
        )
        cls.campaign_hub.add_child(instance=cls.campaign_page_1)
        
        cls.campaign_page_2 = CampaignPage(
            title="Campaign 2",
            slug="campaign-2",
            description="<p>Test description 2</p>",
            summary="<p>Test summary 2</p>",
            image=cls.test_image,
            taxonomy_json='[{"code": "health:pharmacy", "label": "Pharmacy"}]'
        )
        cls.campaign_hub.add_child(instance=cls.campaign_page_2)
        
        cls.resource_page = ResourcePage(
            title="Resource 1",
            slug="resource-1",
            description="<p>Test resource description</p>",
            summary="Test resource summary",
            taxonomy_json='[]'
        )
        root.add_child(instance=cls.resource_page)

    def test_parse_tags_json(self):
        """parse_tags_json should parse valid JSON and handle invalid inputs."""
        result = ManageTagsBulkAction.parse_tags_json('{"123": ["tag1", "tag2"]}')
        self.assertEqual(result, {"123": ["tag1", "tag2"]})
        
        for invalid_input in ["invalid json", "", None]:
            self.assertEqual(ManageTagsBulkAction.parse_tags_json(invalid_input), {})

    def test_get_page_tags(self):
        """get_page_tags should return tags for valid page and empty list for invalid inputs."""
        tags = ManageTagsBulkAction.get_page_tags(self.campaign_page_1.id)
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0]['code'], 'health:gp')
        
        for invalid_input in [99999, None]:
            self.assertEqual(ManageTagsBulkAction.get_page_tags(invalid_input), [])

    def test_save_page_tags(self):
        """save_page_tags should update page's taxonomy_json field."""
        new_tags = [{"code": "new:tag", "label": "New Tag"}]
        ManageTagsBulkAction.save_page_tags(self.resource_page, new_tags, self.user)
        
        self.resource_page.refresh_from_db()
        self.assertEqual(json.loads(self.resource_page.specific.taxonomy_json), new_tags)

    def test_track_changes(self):
        """track_changes should track changes with had_changes flag."""
        from unittest.mock import Mock
        action = Mock(change_details=[])
        original = [{"code": "old", "label": "Old"}]
        final = [{"code": "new", "label": "New"}]
        
        ManageTagsBulkAction.track_changes(
            action, self.campaign_page_1, original, final,
            removed=original, added=final, mode='replace', had_changes=True
        )
        
        self.assertEqual(action.change_details[0]['operation_mode'], 'replace')
        self.assertTrue(action.change_details[0]['had_changes'])
        
        ManageTagsBulkAction.track_changes(
            action, self.campaign_page_1, final, final,
            removed=[], added=[], mode='merge', had_changes=False
        )
        
        self.assertFalse(action.change_details[1]['had_changes'])

    def test_remove_tags_from_page_success(self):
        """remove_tags_from_page should remove specified tags."""
        result = ManageTagsBulkAction.remove_tags_from_page(
            self.campaign_page_1,
            {str(self.campaign_page_1.id): ["health:gp"]},
            self.user
        )
        self.assertTrue(result)
        self.campaign_page_1.refresh_from_db()
        remaining = json.loads(self.campaign_page_1.specific.taxonomy_json)
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]['code'], 'health:hospital')

    def test_remove_tags_from_page_not_in_dict(self):
        """remove_tags_from_page should return False when page not in removal dict."""
        result = ManageTagsBulkAction.remove_tags_from_page(
            self.campaign_page_1, {"999": ["tag"]}, self.user
        )
        self.assertFalse(result)

    def test_remove_tags_from_page_tags_dont_exist(self):
        """remove_tags_from_page should return False when tags don't exist on page."""
        result = ManageTagsBulkAction.remove_tags_from_page(
            self.campaign_page_1, {str(self.campaign_page_1.id): ["nonexistent"]}, self.user
        )
        self.assertFalse(result)

    def test_copy_tags_merge_adds_new_tags(self):
        """copy_tags_to_page in merge mode should add new tags."""
        result = ManageTagsBulkAction.copy_tags_to_page(
            self.campaign_page_2,
            [{"code": "health:gp", "label": "GP"}, {"code": "new:tag", "label": "New"}],
            'merge',
            self.user
        )
        self.assertTrue(result)
        self.campaign_page_2.refresh_from_db()
        self.assertEqual(len(json.loads(self.campaign_page_2.specific.taxonomy_json)), 3)

    def test_copy_tags_merge_skips_duplicates(self):
        """copy_tags_to_page in merge mode should skip duplicates and return False."""
        result = ManageTagsBulkAction.copy_tags_to_page(
            self.campaign_page_2,
            [{"code": "health:pharmacy", "label": "Pharmacy"}],
            'merge',
            self.user
        )
        self.assertFalse(result)

    def test_copy_tags_replace_mode(self):
        """copy_tags_to_page in replace mode should replace all tags."""
        result = ManageTagsBulkAction.copy_tags_to_page(
            self.campaign_page_2,
            [{"code": "replaced", "label": "Replaced"}],
            'replace',
            self.user
        )
        self.assertTrue(result)
        self.campaign_page_2.refresh_from_db()
        tags = json.loads(self.campaign_page_2.specific.taxonomy_json)
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]['code'], 'replaced')

    def test_execute_action_remove_mode(self):
        """execute_action should remove tags in remove mode."""
        num_modified, num_failed = ManageTagsBulkAction.execute_action(
            [self.campaign_page_1],
            active_tab='remove',
            tags_to_remove=json.dumps({str(self.campaign_page_1.id): ["health:gp"]}),
            user=self.user
        )
        self.assertEqual((num_modified, num_failed), (1, 0))

    def test_execute_action_copy_mode(self):
        """execute_action should copy tags in copy mode."""
        num_modified, num_failed = ManageTagsBulkAction.execute_action(
            [self.resource_page],
            active_tab='copy',
            source_page_id=self.campaign_page_1.id,
            tag_operation_mode='merge',
            user=self.user
        )
        self.assertEqual((num_modified, num_failed), (1, 0))

    def test_execute_action_error_tracking(self):
        """execute_action should track errors in change_details."""
        from unittest.mock import Mock
        action = Mock(change_details=[])
        with patch.object(ManageTagsBulkAction, 'remove_tags_from_page', side_effect=Exception("Test error")):
            num_modified, num_failed = ManageTagsBulkAction.execute_action(
                [self.campaign_page_1],
                active_tab='remove',
                tags_to_remove='{}',
                user=self.user,
                bulk_action_instance=action
            )
        self.assertEqual((num_modified, num_failed), (0, 1))
        self.assertIn('error', action.change_details[0])
