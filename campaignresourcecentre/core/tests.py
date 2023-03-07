from django.contrib.auth.models import Group, User
from django.test import RequestFactory, TestCase, override_settings
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailTestUtils

from campaignresourcecentre.core.wagtail_hooks import (
    remove_publication_rights_from_nhse_editors,
    __name__ as module_name,
)


@override_settings(RESTRICTED_PUBLISHING_GROUP_NAME="restricted")
class TestPublicationRestrictions(TestCase, WagtailTestUtils):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.create_test_user()
        self.page = Page.objects.first()
        self.group = Group.objects.create(name="restricted")

    def test_publication_allowed_for_non_editors(self):
        request = self.factory.get("/")
        request.user = self.user
        response = remove_publication_rights_from_nhse_editors(request, self.page)
        self.assertIsNone(response)

    def test_publication_denied_for_editors(self):
        request = self.factory.get("/")
        request.user = self.user
        self.user.groups.add(self.group)
        self.user.save()
        response = remove_publication_rights_from_nhse_editors(request, self.page)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode(), "You do not have permission to publish pages"
        )
