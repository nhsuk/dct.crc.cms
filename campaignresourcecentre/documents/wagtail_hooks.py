from django.shortcuts import render
from wagtail.core import hooks
import logging
from campaignresourcecentre.paragon_users.forms import LoginForm
from campaignresourcecentre.paragon_users.helpers.token_signing import unsign


logger = logging.getLogger(__name__)

# Hook to stop unauthorised users from accessing documents
@hooks.register("before_serve_document")
def authorise_users(doc, request):
    # get key from query string
    pageAuth = request.GET.get("a")
    # if Key is present
    if pageAuth != None:
        try:
            pageAuth = unsign(pageAuth, max_age=1860)
        except:
            logger.warning("Malformed key present in download request")
            return render(request, "errors/500.html")
        if pageAuth != "ALL":
            # Check if user is logged in
            if "ParagonUser" in request.session:
                userAuth = request.session["UserDetails"]["ProductRegistrationVar1"]

                # check if page is standard AND the user is standard or uber (higher level)
                if pageAuth == "standard" and (
                    userAuth == "Standard" or userAuth == "uber"
                ):
                    pass

                # check if page is user AND the user is uber
                elif pageAuth == "uber" and userAuth == "uber":
                    pass

                # if no userauth then something is wrong => go to 403
                elif userAuth == None:
                    logger.info("User has no role")
                    return render(request, "errors/403.html")

                else:
                    logger.info("unrecognised key or User role for download request")
                    return render(request, "errors/403.html")

            # not logged in => login page
            else:
                logger.info("non-user attempted to access document")
                login_form = LoginForm(initial={"previous_page": "/"})
                return render(request, "users/login.html", {"form": login_form})

        # if key is 'all' => no check
        else:
            pass
    # No Key => 403
    else:
        logger.info("No key present in download request")
        return render(request, "errors/403.html")
