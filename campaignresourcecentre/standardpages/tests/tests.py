from io import StringIO
import secrets
import string

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.urls import reverse

from campaignresourcecentre.standardpages.forms import ContactUsForm
from campaignresourcecentre.standardpages.views import search_orphans


class ContactUsViewTests(TestCase):
    def test_view_contact_us_form(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ContactUsForm)
        self.assertContains(response, "Contact us")

    def test_submit_empty_form(self):
        response = self.client.post(reverse("contact_us"), {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "first_name", "Enter your first name")
        self.assertFormError(response, "form", "last_name", "Enter your last name")
        self.assertFormError(response, "form", "job_title", "Select your job function")
        self.assertFormError(
            response, "form", "organisation", "Enter your organisation name"
        )
        self.assertFormError(
            response, "form", "organisation_type", "Enter your organisation type"
        )
        self.assertFormError(response, "form", "email", "Enter your email address")
        self.assertFormError(response, "form", "audience", "Enter your audience")
        self.assertFormError(
            response,
            "form",
            "engage_audience",
            "Enter how you plan to engage this audience",
        )
        self.assertFormError(response, "form", "message", "Enter your message")

    def test_submit_valid_form(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "job_title": "director",
            "organisation": "Acme Inc.",
            "organisation_type": "Private",
            "email": "john.doe@example.com",
            "audience": "Unhealthy people",
            "engage_audience": "Provide leaflets",
            "message": "Please provide advice",
        }
        response = self.client.post(reverse("contact_us"), form_data)
        self.assertContains(response, "Thank you")

    def test_submit_spam_field(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "job_title": "director",
            "cat6a": "spam",
            "organisation": "Acme Inc.",
            "organisation_type": "Private",
            "email": "john.doe@example.com",
            "audience": "Unhealthy people",
            "engage_audience": "Provide leaflets",
            "message": "Please provide advice",
        }
        response = self.client.post(reverse("contact_us"), form_data)
        self.assertContains(response, "Contact us")


user_model = get_user_model()


def generate_random_password():  # To satisfy Sonarquvbe security checks
    password = (
        "".join(secrets.choice(string.ascii_lowercase) for _ in range(3))
        + "".join(secrets.choice(string.ascii_uppercase) for _ in range(3))
        + "".join(secrets.choice(string.digits) for _ in range(3))
        + "".join(secrets.choice(string.punctuation) for _ in range(3))
    )
    return password


class SearchOrphansTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = user_model.objects.create_superuser(
            username="admin",
            password=generate_random_password(),
            email="admin@example.com",
        )

    def test_search_orphans(self):
        # Create a request object with a superuser
        request = self.factory.get("/search_orphans/")
        request.user = self.superuser

        # Set up a StringIO to capture the command output
        response_file = StringIO()

        # Call the searchorphans management command
        call_command("searchorphans", stdout=response_file, stderr=response_file)

        # Reset the StringIO position to the beginning
        response_file.seek(0)

        # Call the view function
        response = search_orphans(request)
        response_text = response.content.decode()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertEqual(response_text, response_file.read())

    def test_search_orphans_permission_denied(self):
        # Create a request object with an anonymous user
        request = self.factory.get("/search_orphans/")
        request.user = user_model.objects.create_user(
            username="anon",
            password=generate_random_password(),
            email="admin@example.com",
        )

        # Call the view function and assert for PermissionDenied exception
        with self.assertRaises(PermissionDenied):
            search_orphans(request)
