from os import environ
from io import StringIO
from unittest.mock import patch, Mock

from django.test import TestCase, SimpleTestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from campaignresourcecentre.azurestore.utils import AzureStorage
from campaignresourcecentre.core.management.commands.searchorphans import (
    Command as SearchOrphanCommand,
)
from campaignresourcecentre.search.azure import AzureSearchBackend


class CreateWagtailSuperuserCommandTestCase(TestCase):
    def test_create_superuser(self):
        environ["WAGTAIL_USER"] = "testuser"
        environ["WAGTAIL_PASSWORD"] = "testpassword"
        out = StringIO()
        call_command("createwagtailsuperuser", stdout=out)
        user_model = get_user_model()
        superuser = user_model.objects.get(username="testuser")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("testpassword"))
        self.assertIn("Superuser 'testuser' created", out.getvalue())

    def test_update_superuser(self):
        user_model = get_user_model()
        user_model.objects.create_superuser(
            username="testuser",
            email="noone@example.com",
            password="testpassword",
        )
        environ["WAGTAIL_USER"] = "testuser"
        environ["WAGTAIL_PASSWORD"] = "newpassword"
        out = StringIO()
        call_command("createwagtailsuperuser", stdout=out)
        updated_superuser = user_model.objects.get(username="testuser")
        self.assertTrue(updated_superuser.check_password("newpassword"))
        self.assertIn("Superuser 'testuser' updated", out.getvalue())

    def test_no_wagtail_user(self):
        environ.pop("WAGTAIL_USER", None)
        out = StringIO()
        call_command("createwagtailsuperuser", stdout=out)
        self.assertIn(
            "No WAGTAIL_USER symbol in environment - no superuser created",
            out.getvalue(),
        )

    def test_no_wagtail_password(self):
        environ["WAGTAIL_USER"] = "testuser"
        environ.pop("WAGTAIL_PASSWORD", None)
        out = StringIO()
        call_command("createwagtailsuperuser", stdout=out)
        self.assertIn(
            "No WAGTAIL_PASSWORD symbol in environment - no superuser created",
            out.getvalue(),
        )
        user_model = get_user_model()
        with self.assertRaises(user_model.DoesNotExist):
            user_model.objects.get(username="testuser")


class TestSearchOrphans(SimpleTestCase):
    def test_search_orphans(self):
        # Sustained effort failed to find a way to mock Azure Storage to test
        # the urls and delete paths through searchorpans
        # This relies on the searchorphans command being able to go through the motions
        err = StringIO()
        out = StringIO()
        call_command("searchorphans", stderr=err, stdout=out)
        err_message = err.getvalue()
        out_message = out.getvalue()
        self.assertTrue(err_message or out_message)
