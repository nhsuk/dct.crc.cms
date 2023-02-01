from importlib import import_module
from unittest.mock import Mock

from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import PermissionDenied
from django.conf import settings as django_settings

from campaignresourcecentre.paragon_users.helpers.token_signing import sign
from .wagtail_hooks import authorise_users


# per https://gist.github.com/dustinfarris/4982145
class SessionEnabledTestCase(TestCase):
    def get_session(self):
        if self.client.session:
            session = self.client.session
        else:
            engine = import_module(django_settings.SESSION_ENGINE)
            session = engine.SessionStore()
        return session

    def set_session_cookies(self, session):
        # Set the cookie to represent the session
        session_cookie = django_settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie] = session.session_key
        cookie_data = {
            "max-age": None,
            "path": "/",
            "domain": django_settings.SESSION_COOKIE_DOMAIN,
            "secure": django_settings.SESSION_COOKIE_SECURE or None,
            "expires": None,
        }
        self.client.cookies[session_cookie].update(cookie_data)

    def make_mock_request(self):
        request = HttpRequest()
        request.META["SERVER_NAME"] = "localhost"
        request.META["SERVER_PORT"] = 8000

        request.session = self.get_session()

        return request


class TestAuthoriseUsers(SessionEnabledTestCase):
    def test_with_no_key(self):
        # create a request with no key

        request = self.make_mock_request()
        request.GET = {}

        # create a mock document
        doc = Mock()

        # call the hook function
        result = authorise_users(doc, request)

        # check that the function returned a bad request
        assert isinstance(result, HttpResponseBadRequest)

    def test_with_malformed_key(self):
        # create a request with a malformed key
        request = self.make_mock_request()
        request.GET = {"a": "invalidkey"}

        # create a mock document
        doc = Mock()

        # call the hook function
        result = authorise_users(doc, request)

        # check that the function returned a bad request
        assert isinstance(result, HttpResponseBadRequest)

    def test_with_valid_key_and_unauthenticated_user(self):
        # create a request with a valid key requiring an uber user
        request = self.make_mock_request()
        request.GET = {"a": sign("uber").decode()}

        # create a mock document
        doc = Mock()

        # call the hook function
        result = authorise_users(doc, request)

        # check that the function returned a redirect to the login page
        assert isinstance(result, HttpResponseRedirect)

    def test_with_valid_key_and_unauthorised_user(self):
        # create a request with a valid key requiring an Uber user
        # but user is only standard
        request = self.make_mock_request()
        request.session["ParagonUser"] = "whatever"
        request.session["UserDetails"] = {"ProductRegistrationVar1": "standard"}
        request.GET = {"a": sign("uber").decode()}

        # create a mock document
        doc = Mock()

        # call the hook function, expecting failure
        with self.assertRaises(PermissionDenied):
            authorise_users(doc, request)

    def test_with_valid_key_and_unregistered_user(self):
        # create a request with a valid key requiring ab Uber user
        request = self.make_mock_request()
        request.session["ParagonUser"] = "whatever"
        request.session["UserDetails"] = {"ProductRegistrationVar1": ""}
        request.GET = {"a": sign("uber").decode()}

        # create a mock document
        doc = Mock()

        # call the hook function, expecting failure
        with self.assertRaises(PermissionDenied):
            authorise_users(doc, request)

    def test_with_valid_key_and_uber_user(self):
        # create a request with a valid key requiring an Uber user
        request = self.make_mock_request()
        request.session["ParagonUser"] = "whatever"
        request.session["UserDetails"] = {"ProductRegistrationVar1": "uber"}
        request.GET = {"a": sign("uber").decode()}

        # create a mock document
        doc = Mock()

        # call the hook function, should be o problem

        authorise_users(doc, request)
