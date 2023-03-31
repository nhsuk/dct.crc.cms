import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from wagtail.core.models import Page


from campaignresourcecentre.apps import CRCV3Config

userModel = get_user_model()


class MonkeyPatchCanUnpublishTestCase(TestCase):
    def setUp(self):
        self.nhse_editors_group = Group.objects.create(name="NHSE Editors")
        self.superuser = userModel.objects.create_superuser(
            username="superuser", email="superuser@test.com", password="test"
        )
        self.editor = userModel.objects.create_user(
            username="editor", email="editor@test.com", password="test", is_active=True
        )
        self.editor.groups.add(self.nhse_editors_group)
        self.non_editor = userModel.objects.create_user(
            username="non_editor",
            email="non_editor@test.com",
            password="test",
            is_active=True,
        )
        self.page = Page(title="Test Page", slug="test-page", path="test", depth=2)
        self.page.live = True
        self.page.save()

    def test_superuser_can_unpublish(self):
        permission_tester = self.page.permissions_for_user(self.superuser)
        self.assertTrue(permission_tester.can_unpublish())

    def test_editor_can_unpublish(self):
        permission_tester = self.page.permissions_for_user(self.editor)
        self.assertTrue(permission_tester.can_unpublish())

    def test_non_editor_cannot_unpublish(self):
        permission_tester = self.page.permissions_for_user(self.non_editor)
        self.assertFalse(permission_tester.can_unpublish())

    def test_inactive_user_cannot_unpublish(self):
        self.editor.is_active = False
        self.editor.save()
        permission_tester = self.page.permissions_for_user(self.editor)
        self.assertFalse(permission_tester.can_unpublish())
