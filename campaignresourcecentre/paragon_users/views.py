from datetime import date 
from logging import getLogger
from urllib.parse import quote

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.utils import timezone

from campaignresourcecentre.notifications.adapters import gov_notify_factory
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError
from campaignresourcecentre.paragon_users.decorators import (
    paragon_user_logged_in,
    paragon_user_logged_out,
)

from .forms import (
    LoginForm,
    NewsLetterPreferencesForm,
    PasswordResetForm,
    PasswordSetForm,
    RegisterForm,
)
from .helpers.newsletter import deserialise, serialise
from .helpers.postcodes import get_region
from .helpers.token_signing import sign, unsign
from .helpers.verification import send_verification

logger = getLogger()


def ParseError(error):
    error_dict = {
        "Account for this email address already exists": [
            "email",
            "Account for this email address already exists",
        ],
        "Email address not valid": ["email", "Email address is not valid"],
        "Password must be at least 6 characters and contain a number": [
            "password",
            "Password must be at least 9 characters long, and contain at least 1 number, 1 capital letter, 1 lowercase letter and 1 symbol",
        ],
        "UserToken can't be null or empty": [None, "Unexpected Error Occured"],
    }
    if error_dict.get(error) is not None:
        parsed = [error_dict.get(error)[0], error_dict.get(error)[1]]
    else:
        parsed = [None, error]
    return parsed


@paragon_user_logged_out
def signup(request):
    if request.method == "POST":
        f = RegisterForm(request.POST)

        organisation = f.fields["organisation"]
        job_title = f.fields["job_title"]
        if not f.data["job_title"] == "student":
            organisation.required = True
            job_title.required = True

        if f.is_valid():
            email = f.cleaned_data.get("email")
            password = f.cleaned_data.get("password")
            first_name = f.cleaned_data.get("first_name")
            last_name = f.cleaned_data.get("last_name")

            if f.cleaned_data.get("job_title") == "health":
                job_title = f.cleaned_data.get("area_work")
            else:
                job_title = f.cleaned_data.get("job_title")
            if not job_title == "student":
                organisation = f.cleaned_data.get("organisation")
            else:
                organisation = " "
            postcode = f.data["postcode"]

            # Need to set created_at (ProductRegistrationVar10) when creating a new user
            # Paragon sets its own created_at field but this is only available from the
            # Search API and not from the RetrieveProfile API
            now = timezone.now()
            created_at = now.strftime("%Y-%m-%dT%H:%M:%S")

            paragon_client = Client()
            try:
                response = paragon_client.create_account(
                    email,
                    password,
                    first_name,
                    last_name,
                    organisation,
                    job_title,
                    postcode,
                    created_at,
                )

                if response["code"] == 200:

                    # Send verification Email
                    token = response["content"]
                    url = request.build_absolute_uri(reverse("verification"))
                    send_verification(token, url, email, first_name)

                    return render(
                        request,
                        "users/confirmation_registration.html",
                        {"email": settings.PHE_PARTNERSHIPS_EMAIL},
                    )
                else:
                    # Report the failure and return a server error
                    logger.error("Failed to create account: %s" % (response,))
                    return HttpResponseServerError()
            except ParagonClientError as PCE:
                for error in PCE.args:
                    paresedError = ParseError(error)
                    f.add_error(paresedError[0], paresedError[1])
                return render(request, "users/signup.html", {"form": f})
    else:
        f = RegisterForm()

    return render(request, "users/signup.html", {"form": f})


@paragon_user_logged_in
def resend_verification(request):
    try:
        client = Client()
        user_token = request.session.get("ParagonUser")
        user = client.get_user_profile(user_token).get("content")
        verified = user.get("ProductRegistrationVar2")
        if verified == "True":
            return redirect("/")
        name = user.get("FirstName")
        email = user.get("EmailAddress")
        url = request.build_absolute_uri(reverse("verification"))
        send_verification(user_token, url, email, name)
    except ParagonClientError as PCE:  # noqa
        return redirect("/")  # put an error page here? 5xx?

    return redirect("/")


def verification(request):
    if request.GET.get("q"):

        # unsign Token from URL Query
        try:
            unsignedToken = unsign(request.GET.get("q"), max_age=86400)
        except Exception as e:
            logging.error ("Failed to unsign token: %s" % (e,))
            return HTTPResponseBadRequest()
        todays_date = date.today().strftime("%d/%m/%Y")
        # set user parameters
        client = Client()
        client_user = client.get_user_profile(unsignedToken)["content"]
        verified = client_user.get("ProductRegistrationVar2")
        if verified != "True":
            email = client_user["EmailAddress"]
            user_job = client_user["ProductRegistrationVar4"]
            postcode = client_user["ProductRegistrationVar9"]

            # update role
            if client.update_user_profile(
                user_token=unsignedToken,
                role=get_role(email, user_job),
                active="True",
                verified_at=todays_date,
                postcode=postcode + "|" + get_region(postcode),
            ):
                if request.session.get("ParagonUser") is unsignedToken:
                    request.session["Verified"] = "True"
                return render(request, "users/confirmation_user_verification.html")
            else:
                return HttpResponseServerError()
    return redirect("/")


def get_role(userEmail: str, userJob: str):
    userEmail = userEmail.lower()
    if (userEmail.endswith("@nhs.net") or userEmail.endswith("@gov.uk")) and (
        userJob == "comms" or userJob == "health:improvement" or userJob == "marketing"
    ):

        return "Uber"
    else:
        return "Standard"


@paragon_user_logged_out
def login(request):

    if request.method == "GET":
        next_url = request.GET.get("next")
        if request.META.get("HTTP_REFERER") is not None:
            login_form = LoginForm(
                initial={
                    "previous_page": next_url
                    if next_url
                    else request.META.get("HTTP_REFERER")
                }
            )
        else:
            login_form = LoginForm(initial={"previous_page": "/"})

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data.get("email")
            password = login_form.cleaned_data.get("password")
            paragon_client = Client()
            try:
                response = paragon_client.login(email, password)

                if response["code"] == 200:
                    request.session.set_test_cookie()
                    if request.session.test_cookie_worked():
                        request.session.delete_test_cookie()  # Check if we can use cookies in the browser

                        user_token = response.get("content")
                        # set user token to Session Cookie
                        request.session["ParagonUser"] = user_token
                        user = paragon_client.get_user_profile(
                            request.session.get("ParagonUser")
                        )["content"]
                        # TODO ideally we'd pass the returned user details through the User dataclass
                        request.session["UserDetails"] = user

                        # add verified status to Session Cookie
                        verified = (
                            paragon_client.get_user_profile(user_token)
                            .get("content")
                            .get("ProductRegistrationVar2")
                        )
                        request.session["Verified"] = verified

                        if verified == "True":
                            return redirect(
                                login_form.cleaned_data.get("previous_page")
                            )
                        else:
                            return render(request, "users/not_verified.html")
                    else:
                        logger.error ("Couldn't set test cookie")
                        return HttpResponseServerError()
                    return redirect("/")
            except ParagonClientError as PCE:
                for error in PCE.args:
                    paresedError = ParseError(error)
                    if paresedError[0] is None:
                        login_form.add_error(None, paresedError[1])
                    else:
                        login_form.add_error(paresedError[0], paresedError[1])
                return render(request, "users/login.html", {"form": login_form})
    return render(request, "users/login.html", {"form": login_form})


@paragon_user_logged_in
def logout(request):
    try:
        request.session.flush()
    except Exception as e:
        logger.error("Exception flushing session: %s", e)
    if request.META.get("HTTP_REFERER") is not None:
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        return redirect("/")


def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)

        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data.get("email").lower()
            paragon_client = Client()
            try:
                response = paragon_client.search_users(email, limit=1)

                response_content = response["content"]

                for dict_item in response_content:
                    if dict_item.get("EmailAddress").lower() == email:
                        userToken = dict_item.get("UserToken")
                        firstName = dict_item.get("FirstName")
                    break
                else:
                    logger.error("Paragon returned no results for email")
                    return HttpResponseServerError

                signedToken = sign(userToken)
                url = (
                    request.build_absolute_uri(reverse("password-set"))
                    + "?q="
                    + quote(signedToken)
                )

                # send confirmation email
                emailClient = (
                    gov_notify_factory()
                )  # This needs to be changed before release
                emailClient.reset_password(email, firstName, url)
                return render(
                    request,
                    "users/confirmation_password_reset.html",
                    {"email": email},
                )
            except ParagonClientError as PCE:
                for error in PCE.args:
                    paresedError = ParseError(error)
                    if paresedError[0] is None:
                        password_reset_form.add_error(None, paresedError[1])
                    else:
                        password_reset_form.add_error(paresedError[0], paresedError[1])
                return render(
                    request,
                    "users/password_reset.html",
                    {"form": password_reset_form},
                )
    else:
        password_reset_form = PasswordResetForm()

    return render(
        request,
        "users/password_reset.html",
        {"form": password_reset_form},
    )


def password_set(request):
    if request.GET.get("q"):
        paragon_client = Client()
        # We use this to check if the user token is valid for unsigning
        try:
            user_token = unsign(request.GET.get("q"), max_age=86400)
        except Exception as e:  # noqa
            logger.error("Failed to unsign user token: %s" % e)
            return HttpResponseBadRequest()
        # Check if the user token returns a profile to authenticate it
        user_profile = paragon_client.get_user_profile(user_token)
        status = user_profile.get("code")
        if status == 200:
            if request.method == "POST":
                password_set_form = PasswordSetForm(request.POST)

                if password_set_form.is_valid():
                    password = password_set_form.cleaned_data.get("password")
                    password_check = password_set_form.cleaned_data.get(
                        "password_check"
                    )

                    if password == password_check:
                        try:
                            response = paragon_client.update_password(
                                user_token, password
                            )

                            if response["content"] is True:
                                return render(
                                    request, "users/confirmation_password_set.html"
                                )
                            else:
                                return redirect("/password-set")

                        except ParagonClientError as PCE:
                            for error in PCE.args:
                                paresedError = ParseError(error)
                                if paresedError[0] is None:
                                    password_set_form.add_error(None, paresedError[1])
                                else:
                                    password_set_form.add_error(
                                        paresedError[0], paresedError[1]
                                    )
                            return render(
                                request,
                                "users/password_set.html",
                                {"form": password_set_form},
                            )
                    else:
                        password_set_form.add_error(None, "Passwords do not match.")

            else:
                password_set_form = PasswordSetForm()

            return render(
                request, "users/password_set.html", {"form": password_set_form}
            )
        else:
            logger.error("Paragon API returned status code %d", status)
            return HttpResponseBadRequest()
    else:
        logger.error("Password set requested without user token")
        return HttpResponseBadRequest()
    return redirect("/")


@paragon_user_logged_in
def user_profile(request):
    paragon_client = Client()
    user = paragon_client.get_user_profile(request.session.get("ParagonUser"))[
        "content"
    ]

    job_choices = {
        "director": "Director / Board Member / CEO",
        "admin": "Administration",
        "comms": "Communications",
        "education": "Education and Teaching",
        "marketing": "Marketing",
        "hr": "HR / Training / Organisational Development",
        "community": "Community and Social Services / Charity / Volunteering",
        "student": "Student / Unemployed / Retired",
        "health": "Health",
        "other": "Other",
        "health:other": "Other",
        "health:improvement": "Health Improvement / Public Health",
        "health:gpspecialistnurse": "GP, Specialist, Nurse and HCA",
        "health:pharmacy": "Pharmacy",
        "health:management": "Practice Management",
    }

    context = {
        "first_name": user["FirstName"],
        "last_name": user["LastName"],
        "email_address": user["EmailAddress"],
        "organisation": user["ProductRegistrationVar3"],
        "job_title": job_choices.get(user["ProductRegistrationVar4"]),
        "postcode": user["ProductRegistrationVar9"].split("|")[0],
        "user_type": user["ProductRegistrationVar1"],
    }

    return render(request, "users/account.html", context)


@paragon_user_logged_in
def newsletter_preferences(request):
    paragon_client = Client()
    client_user = paragon_client.get_user_profile(request.session.get("ParagonUser"))[
        "content"
    ]
    newsletters = deserialise(client_user["ProductRegistrationVar7"])

    if request.method == "POST":
        newsletter_form = NewsLetterPreferencesForm(request.POST)

        if newsletter_form.is_valid():
            newsletters_form = dict(newsletter_form.cleaned_data)
            serialised_newsletters = serialise(newsletters_form)

            try:
                paragon_client.update_user_profile(
                    user_token=request.session.get("ParagonUser"),
                    subscriptions=serialised_newsletters,
                )
                # Find all items that haven't changed or have the value of False
                unchanged_data = [
                    k for k in newsletters_form if newsletters_form.get(k) is False
                ]
                for k in unchanged_data:
                    del newsletters_form[k]

                # Fetch label attribute from form.field object (stored in forms.py)
                newsletters_cleaned = [
                    newsletter_form.fields.get(key).label
                    for key in newsletters_form.keys()
                ]

                return render(
                    request,
                    "users/confirmation_newsletters.html",
                    {"preferences": newsletters_cleaned},
                )
            except ParagonClientError as PCE:
                for error in PCE.args:
                    paresedError = ParseError(error)
                    if paresedError[0] is None:
                        newsletter_form.add_error(None, paresedError[1])
                    else:
                        newsletter_form.add_error(paresedError[0], paresedError[1])
            return render(
                request,
                "users/newsletter_preferences.html",
                {"form": newsletter_form},
            )
    else:
        newsletter_form = NewsLetterPreferencesForm(initial=newsletters)

        return render(
            request,
            "users/newsletter_preferences.html",
            {"form": newsletter_form},
        )


@paragon_user_logged_in
def order_history(request):
    paragon_client = Client()
    todays_date = date.today().strftime("%d/%m/%Y")

    data = (
        paragon_client.order_history(
            request.session.get("ParagonUser"),
            "01/01/2020",
            str(todays_date),
            "1",
            "1000",
        )
        .get("content")
        .get("Orders")
    )
    sort = request.POST.get("sort")
    if sort:
        if sort == "oldest":
            data = sorted(data, key=lambda k: k["OrderDate"])
        elif sort == "recent":
            data = sorted(data, key=lambda k: k["OrderDate"], reverse=True)

    return render(
        request,
        "users/order_history.html",
        {"data": data, "sort": sort}
        # We pass the sort back into the template to ensure the current sort option is the default on page load
    )
