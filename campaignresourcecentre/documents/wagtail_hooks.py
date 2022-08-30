from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.signing import BadSignature
from wagtail.core import hooks

from cryptography.fernet import InvalidToken

from campaignresourcecentre.paragon_users.helpers.token_signing import unsign
from campaignresourcecentre.paragon_users.forms import ROLE_CHOICES

import logging

logger = logging.getLogger(__name__)

# Hook to stop unauthorised users from accessing documents
@hooks.register("before_serve_document")
def authorise_users(doc, request):
    # get key from query string
    pageAuth = request.GET.get("a")
    # if Key is present
    if pageAuth is None:
        logger.warning("No key present in download request")
        raise SuspiciousOperation(request, "No key")
    else:
        try:
            pageAuth = unsign(pageAuth).lower()
        except (BadSignature, InvalidToken):
            logger.warning("Malformed key present in download request")
            raise SuspiciousOperation(request, "Malformed key")
        # if document not universally available, need to check authorisation
        if pageAuth != "all":
            # Check if user is logged in
            if "ParagonUser" in request.session:
                userAuth = (
                    request.session["UserDetails"]["ProductRegistrationVar1"] or ""
                ).lower()
                if userAuth:
                    if userAuth in (r[0] for r in ROLE_CHOICES):
                        # check if page is standard AND the user is standard or uber (higher level) OR
                        # page is uber and user is uber
                        if (
                            pageAuth == "standard"
                            and (userAuth == "standard" or userAuth == "uber")
                        ) or (pageAuth == "uber" and userAuth == "uber"):
                            return  # A null response is OK
                        else:
                            raise PermissionDenied
                    else:  # unknown userAuth
                        raise Exception("Invalid userAuth value")
                else:  # Maybe not registered
                    raise PermissionDenied("Username has not been verified")
            # not logged in => return a redirect to login page
            else:
                logger.info("non-user attempted to access document")
                resp = HttpResponseRedirect("/login")
                if "HTTP_REFERER" in request.META.get("HTTP_REFERER", ""):
                    resp["HTTP_REFERER"] = request.META.get("HTTP_REFERER")
                return resp
