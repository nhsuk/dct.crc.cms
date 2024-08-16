from io import StringIO
import secrets
import string

from django.contrib.auth import get_user_model
from django.test import TestCase
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

        errors = [
            "Enter your first name",
            "Enter your last name",
            "Select your job function",
            "Enter your organisation name",
            "Enter your organisation type",
            "Enter your email address",
            "Enter your audience",
            "Enter how you plan to engage this audience",
            "Enter your message",
        ]

        for error in errors:
            print("Checking for : ", error)
            self.assertContains(response, error)

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
