from os import environ
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class CreateWagtailSuperuserCommandTestCase(TestCase):
    def test_create_superuser(self):
        environ["WAGTAIL_USER"] = "testuser"
        environ["WAGTAIL_PASSWORD"] = "testpassword"
        out = StringIO()
        call_command("createwagtailsuperuser", stdout=out)
        userModel = get_user_model()
        superuser = userModel.objects.get(username="testuser")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("testpassword"))
        self.assertIn("Superuser 'testuser' created", out.getvalue())

    def test_update_superuser(self):
        userModel = get_user_model()
        superuser = userModel.objects.create_superuser(
            username="testuser",
            email="noone@example.com",
            password="testpassword",
        )
        environ["WAGTAIL_USER"] = "testuser"
        environ["WAGTAIL_PASSWORD"] = "newpassword"
        out = StringIO()
        call_command("createwagtailsuperuser", stdout=out)
        updated_superuser = userModel.objects.get(username="testuser")
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
        userModel = get_user_model()
        with self.assertRaises(userModel.DoesNotExist):
            userModel.objects.get(username="testuser")
