from unittest.mock import patch
from django.test import TestCase


class ValidatePostcodeTestCase(TestCase):

    @patch("campaignresourcecentre.paragon_users.forms.get_postcode_region")
    def test_valid_postcode_formats(self, mock_get_region):
        from campaignresourcecentre.paragon_users.forms import validate_postcode

        mock_get_region.return_value = "London"
        valid_postcodes = [
            "SW1A 1AA",
            "SW1A1AA",
            "M1 1AA",
            "B33 8TH",
            "W1A 0AX",
            "sw1a 1aa",
            " SW1A 1AA ",
        ]

        for postcode in valid_postcodes:
            with self.subTest(postcode=postcode):
                try:
                    validate_postcode(postcode)
                except Exception as e:
                    self.fail(f"Valid postcode '{postcode}' raised exception: {e}")

    def test_invalid_postcode_formats(self):
        from campaignresourcecentre.paragon_users.forms import validate_postcode
        from django.core.exceptions import ValidationError

        invalid_postcodes = [
            "",
            "INVALID",
            "12345",
            "SW1A",
            "SW1A 1AAA",
            "SW1A1A",
            "1W1A 1AA",
            "SW1AA 1AA",
        ]

        for postcode in invalid_postcodes:
            with self.subTest(postcode=postcode):
                with self.assertRaises(ValidationError) as context:
                    validate_postcode(postcode)
                self.assertIn("not in the correct format", str(context.exception))

    @patch("campaignresourcecentre.paragon_users.forms.get_postcode_region")
    def test_postcode_not_found_in_api(self, mock_get_region):
        from campaignresourcecentre.paragon_users.forms import validate_postcode
        from campaignresourcecentre.paragon_users.helpers.postcodes import (
            PostcodeException,
        )
        from django.core.exceptions import ValidationError

        mock_get_region.side_effect = PostcodeException("Postcode not found")

        with self.assertRaises(ValidationError) as context:
            validate_postcode("SW1A 1AA")
        self.assertIn("not recognised", str(context.exception))

    @patch("campaignresourcecentre.paragon_users.forms.get_postcode_region")
    def test_postcode_api_error(self, mock_get_region):
        from campaignresourcecentre.paragon_users.forms import validate_postcode
        from campaignresourcecentre.paragon_users.helpers.postcodes import (
            PostcodeException,
        )
        from django.core.exceptions import ValidationError

        mock_get_region.side_effect = PostcodeException("API request failed")

        with self.assertRaises(ValidationError) as context:
            validate_postcode("SW1A 1AA")
        self.assertIn("not recognised", str(context.exception))
