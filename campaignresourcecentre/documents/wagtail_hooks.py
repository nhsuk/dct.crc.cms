from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, BadRequest, SuspiciousOperation
from django.core.signing import BadSignature
from wagtail import hooks

from cryptography.fernet import InvalidToken

from campaignresourcecentre.paragon_users.helpers.token_signing import unsign
from campaignresourcecentre.paragon_users.forms import ROLE_CHOICES
from campaignresourcecentre.utils.views import bad_request

import logging

logger = logging.getLogger(__name__)


def _get_key(request):
    page_auth = request.GET.get("a")
    if page_auth is None:
        logger.warning("No key present in download request")
        raise ValueError("No key")
    try:
        return unsign(page_auth).lower()
    except (BadSignature, InvalidToken):
        logger.warning("Malformed key present in download request")
        raise ValueError("Malformed key")


def _get_user_auth(request):
    if "ParagonUser" in request.session:
        user_auth = (
            request.session["UserDetails"]["ProductRegistrationVar1"] or ""
        ).lower()
        if user_auth:
            if user_auth in (r[0] for r in ROLE_CHOICES):
                return user_auth
            else:
                logger.error("Invalid user_auth value '%s'", user_auth)
                raise ValueError("Invalid user_auth value")
        else:
            return "unverified"
    else:
        raise PermissionDenied("User has not signed in")


def _is_authorized(page_auth, user_auth):
    if page_auth == "all":
        return True
    if page_auth == "standard" and (user_auth == "standard" or user_auth == "uber"):
        return True
    if page_auth == "uber" and user_auth == "uber":
        return True
    return False


# Hook to stop unauthorised users from accessing documents
@hooks.register("before_serve_document")
def authorise_users(doc, request):
    # Attempt to get authority required for page
    try:
        page_auth = _get_key(request)
    except ValueError as e:
        return bad_request(request, str(e))

    # Attempt to established user status
    try:
        user_auth = _get_user_auth(request)
    except PermissionDenied:
        logger.info("non-user attempted to access document")
        resp = HttpResponseRedirect("/login")
        if "HTTP_REFERER" in request.META.get("HTTP_REFERER", ""):
            resp["HTTP_REFERER"] = request.META.get("HTTP_REFERER")
        return resp

    # Check page requirement against user status
    if not _is_authorized(page_auth, user_auth):
        raise PermissionDenied
