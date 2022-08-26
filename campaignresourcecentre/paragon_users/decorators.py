from functools import wraps
from logging import getLogger

from django.shortcuts import redirect, render
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError

logger = getLogger(__name__)

# These decorators may be called with or without arguments and the name/doc string
# will be preserved.


def verified_user(
    view_func=None,
    url=None,
    require_logged_in=True,
    require_logged_in_and_verified=True,
):
    # Allows decorator to be used without arguments
    assert callable(view_func) or view_func is None

    def _decorator(func):
        @wraps(func)
        def _wrapped_view_function(*args, **kwargs):
            redirect_url = url
            request = args[0]
            logged_in = "ParagonUser" in request.session
            if redirect_url is None:
                redirect_url = "/" if logged_in else "/login/"
            if logged_in:
                good_to_go = require_logged_in

                if good_to_go and require_logged_in_and_verified:
                    # If don't have the Verified cookie, get one.
                    # This should not happen anywhere this decorator is used
                    if "Verified" not in request.session:
                        try:
                            client = Client()
                            user = client.get_user_profile(
                                request.session.get("ParagonUser")
                            )
                        except ParagonClientError as PCE:
                            logger.error("Paragon error: %s" % PCE)
                            raise Exception("User lookup failed")
                        request.session["Verified"] = user.get(
                            "ProductRegistrationVar2"
                        )
                    verified = request.session.get("Verified") == "True"
                    good_to_go = verified
                    if not good_to_go:
                        return render(request, "users/not_verified.html")
            else:
                good_to_go = not require_logged_in

            if good_to_go:
                return func(*args, **kwargs)
            else:
                onward_query = "?next=" + request.path if require_logged_in else ""
                return redirect(redirect_url + onward_query)

        return _wrapped_view_function

    return _decorator(view_func) if view_func else _decorator


def paragon_user_logged_in(view_func=None, url=None):
    return verified_user(view_func, url=url)


def paragon_user_logged_out(view_func=None, url=None):
    return verified_user(view_func, url=url, require_logged_in=False)
