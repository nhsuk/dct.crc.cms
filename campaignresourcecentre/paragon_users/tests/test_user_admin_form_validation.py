from django.test import TestCase

from campaignresourcecentre.paragon_users.forms import UserAdminForm


class UserAdminFormValidationTestCase(TestCase):
    def _build_form(self, **overrides):
        data = {
            "role": "standard",
            "email": "admin@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "organisation": "Example Org",
            "job_title": "other",
            "postcode": "LS1 1AA",
        }
        data.update(overrides)

        initial = {
            "verified_at": "2025-01-01T00:00:00",
            "job_title": data["job_title"],
        }

        return UserAdminForm(data=data, initial=initial, all_fields_editable=True)

    def test_health_job_title_requires_health_role(self):
        form = self._build_form(job_title="health")

        self.assertFalse(form.is_valid())
        self.assertIn("health_role", form.errors)
        self.assertIn("Select a health role", form.errors["health_role"])

    def test_education_job_title_requires_education_role(self):
        form = self._build_form(job_title="education")

        self.assertFalse(form.is_valid())
        self.assertIn("education_role", form.errors)
        self.assertIn("Select an education role", form.errors["education_role"])

    def test_health_job_title_with_health_role_is_valid(self):
        form = self._build_form(job_title="health", health_role="health:gp")

        self.assertTrue(form.is_valid())

    def test_education_job_title_with_education_role_is_valid(self):
        form = self._build_form(
            job_title="education", education_role="education:teacher"
        )

        self.assertTrue(form.is_valid())
