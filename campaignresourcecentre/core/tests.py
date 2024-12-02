import unittest
from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory

from campaignresourcecentre.core.helpers import verify_pubtoken


class VerifyPubTokenTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch.object(settings, "PUBTOKEN", "valid_token")
    def test_verify_pubtoken_valid(self):
        request = self.factory.get("/", headers={"AdminToken": "valid_token"})
        self.assertTrue(verify_pubtoken(request))

    @patch.object(settings, "PUBTOKEN", "valid_token")
    def test_verify_pubtoken_invalid(self):
        request = self.factory.get("/", headers={"AdminToken": "invalid_token"})
        self.assertFalse(verify_pubtoken(request))

    @patch.object(settings, "PUBTOKEN", None)
    def test_verify_pubtoken_no_token(self):
        request = self.factory.get("/")
        self.assertFalse(verify_pubtoken(request))

    def test_verify_pubtoken_no_admintoken_header(self):
        request = self.factory.get("/")
        self.assertFalse(verify_pubtoken(request))
