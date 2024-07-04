from io import StringIO
import secrets
import string

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.urls import reverse

from campaignresourcecentre.standardpages.forms import ContactUsForm
from campaignresourcecentre.standardpages.views import search_orphans, manage_files


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
