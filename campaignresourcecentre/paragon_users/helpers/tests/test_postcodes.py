import json
from unittest.mock import Mock, patch
from django.test import TestCase

from campaignresourcecentre.paragon_users.helpers.postcodes import (
    get_postcode_data,
    get_postcode_region,
    get_region,
    PostcodeException,
)


class PostcodeHelpersTestCase(TestCase):

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.requests")
    def test_get_postcode_data_success(self, mock_requests):
        """Test successful postcode data retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {"postcode": "SW1A 1AA", "region": "London", "country": "England"}
            ]
        }
        mock_requests.get.return_value = mock_response

        result = get_postcode_data("SW1A 1AA")

        self.assertEqual(result["postcode"], "SW1A 1AA")
        self.assertEqual(result["region"], "London")

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.requests")
    def test_get_postcode_data_api_error(self, mock_requests):
        """Test API error handling"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_requests.get.return_value = mock_response

        with self.assertRaises(PostcodeException) as context:
            get_postcode_data("SW1A 1AA")

        self.assertIn("Postcode request failed", str(context.exception))
        self.assertIn("500", str(context.exception))

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.requests")
    def test_get_postcode_data_no_results(self, mock_requests):
        """Test when postcode is not found (empty result)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": []}
        mock_requests.get.return_value = mock_response

        with self.assertRaises(PostcodeException) as context:
            get_postcode_data("INVALID1")

        self.assertEqual(str(context.exception), "Postcode not found")

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.requests")
    def test_get_postcode_data_null_result(self, mock_requests):
        """Test when result is None"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": None}
        mock_requests.get.return_value = mock_response

        with self.assertRaises(PostcodeException) as context:
            get_postcode_data("INVALID2")

        self.assertEqual(str(context.exception), "Postcode not found")

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.requests")
    def test_get_postcode_data_invalid_json(self, mock_requests):
        """Test invalid JSON response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_response.text = "Not JSON"
        mock_requests.get.return_value = mock_response

        with self.assertRaises(PostcodeException) as context:
            get_postcode_data("SW1A 1AA")

        self.assertIn("not a valid JSON response", str(context.exception))

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.get_postcode_data")
    def test_get_postcode_region_success(self, mock_get_data):
        """Test successful region retrieval"""
        mock_get_data.return_value = {"region": "London"}

        result = get_postcode_region("SW1A 1AA")

        self.assertEqual(result, "London")

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.get_postcode_data")
    def test_get_postcode_region_error(self, mock_get_data):
        """Test region retrieval error handling"""
        mock_get_data.side_effect = PostcodeException("Postcode not found")

        with self.assertRaises(PostcodeException) as context:
            get_postcode_region("INVALID")

        self.assertIn("Failed to retrieve postcode region", str(context.exception))

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.get_postcode_region")
    def test_get_region_known_region(self, mock_get_region):
        """Test region mapping for known regions"""
        mock_get_region.return_value = "London"

        result = get_region("SW1A 1AA")

        self.assertEqual(result, "region.london")

    @patch("campaignresourcecentre.paragon_users.helpers.postcodes.get_postcode_region")
    def test_get_region_unknown_region(self, mock_get_region):
        """Test region mapping for unknown regions"""
        mock_get_region.return_value = "Unknown Region"

        result = get_region("XX1 1XX")

        self.assertEqual(result, "region.other")
