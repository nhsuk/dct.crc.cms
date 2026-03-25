from unittest.mock import patch

from django.test import TestCase

from campaignresourcecentre.paragon_users.forms import RegisterForm


@patch(
    "campaignresourcecentre.paragon_users.forms.get_postcode_region",
    return_value="London",
)
class ConfirmEmailValidationTestCase(TestCase):
    def get_valid_form_data(self, **overrides):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "confirm_email": "test@example.com",
            "password": "TestPass123@",
            "job_title": "health",
            "health_role": "health:gp",
            "organisation": "Test Org",
            "postcode": "SW1A 1AA",
            "terms": True,
        }
        data.update(overrides)
        return data

    def test_matching_emails_is_valid(self, _mock_postcode):
        form = RegisterForm(self.get_valid_form_data())
        self.assertTrue(form.is_valid())

    def test_mismatched_emails_is_invalid(self, _mock_postcode):
        form = RegisterForm(
            self.get_valid_form_data(confirm_email="different@example.com")
        )
        self.assertFalse(form.is_valid())

    def test_mismatched_emails_adds_error_to_both_fields(self, _mock_postcode):
        form = RegisterForm(
            self.get_valid_form_data(confirm_email="different@example.com")
        )
        form.is_valid()
        self.assertIn("email", form.errors)
        self.assertIn("confirm_email", form.errors)

    def test_mismatched_emails_error_message(self, _mock_postcode):
        form = RegisterForm(
            self.get_valid_form_data(confirm_email="different@example.com")
        )
        form.is_valid()
        self.assertIn("Email addresses must match", form.errors["email"])
        self.assertIn("Email addresses must match", form.errors["confirm_email"])

    def test_missing_confirm_email_is_invalid(self, _mock_postcode):
        data = self.get_valid_form_data()
        del data["confirm_email"]
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("confirm_email", form.errors)

    def test_missing_confirm_email_error_message(self, _mock_postcode):
        data = self.get_valid_form_data()
        del data["confirm_email"]
        form = RegisterForm(data)
        form.is_valid()
        self.assertIn("Confirm email", form.errors["confirm_email"])

    def test_case_insensitive_email_match(self, _mock_postcode):
        form = RegisterForm(
            self.get_valid_form_data(
                email="Test@Example.com", confirm_email="test@example.com"
            )
        )
        self.assertTrue(form.is_valid())
