from django.shortcuts import redirect, render
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError


def paragon_user_logged_in(view_func, url="/login"):
    def _wrapped_view_func(request, *args, **kwargs):
        if "ParagonUser" in request.session:
            return view_func(request, *args, **kwargs)

        else:
            return redirect(url)

    return _wrapped_view_func


def paragon_user_logged_out(view_func, url="/"):
    def _wrapped_view_func(request, *args, **kwargs):
        if "ParagonUser" not in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(url)

    return _wrapped_view_func


def verified_user(view_func, url="/"):
    """
    This requires a user to be logged in, so please user it after a decorator to show that
    """  # should we refactor to allow for this?

    def _wrapped_view_func(request, *args, **kwargs):
        # if dont have the cookie, get one. This Should not happen anywhere this decorator is used
        if "Verified" not in request.session:
            try:
                client = Client()
                user = client.get_user_profile(request.session.get("ParagonUser"))
            except ParagonClientError as PCE:
                return redirect(
                    url
                )  # this should probably go to a specific error page? 401? 5xx?
            request.session["Verified"] = user.get("ProductRegistrationVar2")
        # if you are verified
        if request.session.get("Verified") == "True":
            # the user is directed to the view
            return view_func(request, *args, **kwargs)
        # else it goes to the not verified page
        else:
            render(request, "users/not_verified.html")

    return _wrapped_view_func
