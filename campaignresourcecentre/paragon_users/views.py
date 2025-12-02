from datetime import date
from logging import getLogger
from urllib.parse import quote, urlparse
import json

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.utils import timezone
from django.views import View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from campaignresourcecentre.notifications.adapters import gov_notify_factory
from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import (
    ParagonClientError,
    ParagonClientTimeout,
)
from campaignresourcecentre.paragon_users.decorators import (
    paragon_user_logged_in_unverified,
    paragon_user_logged_in,
    paragon_user_logged_out,
    paragon_user_registering,
)
from campaignresourcecentre.paragon_users.helpers.postcodes import get_postcode_data
from campaignresourcecentre.paragon.helpers.reporting import send_report

from .forms import (
    LoginForm,
    NewsLetterPreferencesForm,
    PasswordResetForm,
    PasswordSetForm,
    RegisterForm,
    EmailUpdatesForm,
    JOB_CHOICES,
    HEALTH_CHOICES,
)
from .helpers.newsletter import (
    deserialise,
    serialise,
    map_school_years_to_primary_and_secondary,
    map_primary_and_secondary_to_school_years,
    map_registration_school_types_to_school_years,
    school_year_groups,
)
from .helpers.postcodes import get_region
from .helpers.token_signing import sign, unsign
from .helpers.verification import send_verification

from campaignresourcecentre.utils.models import FeatureFlags

logger = getLogger(__name__)


def parse_error(error):
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
        if f.data["job_title"] != "student":
            organisation.required = True
            job_title.required = True

        if f.is_valid():
            email = f.cleaned_data.get("email")
            password = f.cleaned_data.get("password")
            first_name = f.cleaned_data.get("first_name")
            last_name = f.cleaned_data.get("last_name")
            job_title = f.cleaned_data.get("job_title")
            area_work = f.cleaned_data.get("area_work")
            organisation = (
                f.cleaned_data.get("organisation") if job_title != "student" else " "
            )
            postcode = f.cleaned_data.get("postcode")
            postcode_region = get_region(postcode)

            # Need to set created_at (ProductRegistrationVar10) when creating a new user
            # Paragon sets its own created_at field but this is only available from the
            # Search API and not from the RetrieveProfile API
            now = timezone.now()
            created_at = now.strftime("%Y-%m-%d %H:%M:%S")

            paragon_client = Client()
            try:
                response = paragon_client.create_account(
                    email,
                    password,
                    first_name,
                    last_name,
                    organisation,
                    job_title,
                    area_work,
                    postcode,
                    postcode_region,
                    created_at,
                )

                if response["code"] == 200:
                    # Send verification Email
                    token = response["content"]
                    url = f"{settings.SITE_BASE_URL}{reverse('verification')}"
                    send_verification(token, url, email, first_name)
                    postcode_data = get_postcode_data(postcode)

                    # send off data to reporting
                    data_dump = json.dumps(
                        {
                            "userToken": token,
                            "createdAt": created_at,
                            "organisation": organisation,
                            "jobTitle": job_title,
                            "role": get_role(email, job_title),
                            "postcode": postcode,
                            "longitude": postcode_data.get("longitude"),
                            "latitude": postcode_data.get("latitude"),
                            "region": postcode_data.get("region"),
                            "date": timezone.now().strftime("%Y-%m-%d"),
                        }
                    )
                    send_report("registration", data_dump)
                    # store user state in session
                    request.session["registration"] = token
                    return redirect("/email_updates")
                else:
                    # Report the failure and return a server error
                    logger.error("Failed to create account: %s" % (response,))
                    return HttpResponseServerError()
            except ParagonClientError as PCE:
                logger.error("Failed to create account: %s" % (json.dumps(PCE.args)))
                for error in PCE.args:
                    this_parse_error = parse_error(error)
                    f.add_error(this_parse_error[0], this_parse_error[1])
                return render(request, "users/signup.html", {"form": f})
    else:
        f = RegisterForm()

    return render(request, "users/signup.html", {"form": f})


@method_decorator(paragon_user_registering, name="dispatch")
class EmailUpdatesView(FormView):
    form_class = EmailUpdatesForm

    def get_template_names(self):
        if FeatureFlags.for_request(self.request).sz_email_variant:
            return ["users/email_updates_variant.html"]
        return ["users/email_updates.html"]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        email_updates = cleaned_data.get("email_updates")

        if email_updates in ("yes", "health"):
            return redirect("/newsletters")

        elif email_updates in ("school"):
            if FeatureFlags.for_request(self.request).sz_email_variant == False:
                raise ValueError("email_updates of school is disabled")

            schools = cleaned_data.get("school_resources_types")
            school_years = map_registration_school_types_to_school_years(schools)

            try:
                Client().update_user_profile(
                    user_token=self.request.session.get("registration"),
                    subscriptions=serialise(school_years),
                )
            except ParagonClientError as pce:
                for error in pce.args:
                    error_message = parse_error(error)
                    form.add_error(error_message[0], error_message[1])
                return render(
                    self.request,
                    "users/email_updates_variant.html",
                    {"form": form},
                )

        elif email_updates in ("no", "none"):
            # No need to do anything
            pass

        else:
            raise NotImplementedError(f"Unknown email_updates: {email_updates}")

        del self.request.session["registration"]
        return render(
            self.request,
            "users/confirmation_registration.html",
            {"email": settings.PHE_PARTNERSHIPS_EMAIL},
        )

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = EmailUpdatesForm(request=self.request)
        return super().get_context_data(**kwargs)


@paragon_user_logged_in_unverified
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
        url = f"{settings.SITE_BASE_URL}{reverse('verification')}"
        send_verification(user_token, url, email, name)
    except ParagonClientError as e:
        logger.error("Failed to retrieve user profile: %s", e)
        return redirect("/")

    return redirect("/")


def verification(request):
    if request.GET.get("q"):
        # unsign Token from URL Query
        try:
            unsigned_token = unsign(request.GET.get("q"), max_age=86400)
        except Exception as e:
            logger.error("Failed to unsign token: %s" % (e,))
            return HttpResponseBadRequest()
        todays_date = date.today().strftime("%Y-%m-%dT%H:%M:%S")
        # set user parameters
        client = Client()
        client_user = client.get_user_profile(unsigned_token)["content"]
        verified = client_user.get("ProductRegistrationVar2")
        if verified != "True":
            email = client_user["EmailAddress"]
            user_job = (
                client_user["ContactVar2"]
                if client_user["ContactVar2"]
                else client_user["ProductRegistrationVar4"]
            )
            postcode = client_user["ProductRegistrationVar9"]

            # update role
            if client.update_user_profile(
                user_token=unsigned_token,
                role=get_role(email, user_job),
                active="True",
                verified_at=todays_date,
                postcode_region=get_region(postcode),
                postcode=postcode,
            ):
                if request.session.get("ParagonUser") == unsigned_token:
                    request.session["Verified"] = "True"
                return render(request, "users/confirmation_user_verification.html")
            else:
                return HttpResponseServerError()
    return redirect("/")


def get_role(user_email: str, user_job: str):
    user_email = user_email.lower()
    if (
        user_email.endswith("@nhs.net")
        or user_email.endswith("@gov.uk")
        or user_email.endswith(".gov.uk")
    ) and (
        user_job == "comms"
        or user_job == "health:improvement"
        or user_job == "marketing"
    ):
        return "uber"
    else:
        return "standard"


@require_http_methods(["POST", "GET"])
@paragon_user_logged_out
def login(request):
    if request.method == "GET":
        next_url = request.GET.get("next")
        if request.META.get("HTTP_REFERER") is not None:
            login_form = LoginForm(
                initial={
                    "previous_page": (
                        next_url if next_url else request.META.get("HTTP_REFERER")
                    )
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
                        logger.error("Couldn't set test cookie")
                        return HttpResponseServerError()
            except ParagonClientTimeout:
                return HttpResponseServerError()
            except ParagonClientError as PCE:
                logger.error("Failed to log user in: %s" % (json.dumps(PCE.args)))
                for error in PCE.args:
                    this_parse_error = parse_error(error)
                    if this_parse_error[0] is None:
                        login_form.add_error(None, this_parse_error[1])
                    else:
                        login_form.add_error(this_parse_error[0], this_parse_error[1])
                return render(request, "users/login.html", {"form": login_form})
    return render(request, "users/login.html", {"form": login_form})


@require_http_methods(["GET"])
def logout(request):
    try:
        request.session.flush()
    except Exception as e:
        logger.error("Exception flushing session: %s", e)
    if request.META.get("HTTP_REFERER") is not None:
        # Redirect user if order is placed and they log out
        if urlparse(request.META.get("HTTP_REFERER")).path == "/orders/place/":
            return redirect("/")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        return redirect("/")


@require_http_methods(["POST", "GET"])
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
                        user_token = dict_item.get("UserToken")
                        first_name = dict_item.get("FirstName")
                    break
                else:
                    logger.error("Paragon returned no results for email")
                    return HttpResponseServerError

                signed_token = sign(user_token)
                url = f"{settings.SITE_BASE_URL}{reverse('password-set')}?q={quote(signed_token)}"

                # send confirmation email
                email_client = (
                    gov_notify_factory()
                )  # This needs to be changed before release
                email_client.reset_password(email, first_name, url)
                return render(
                    request,
                    "users/confirmation_password_reset.html",
                    {"email": email},
                )
            except ParagonClientError as PCE:
                for error in PCE.args:
                    this_parse_error = parse_error(error)
                    if this_parse_error[0] is None:
                        password_reset_form.add_error(None, this_parse_error[1])
                    else:
                        password_reset_form.add_error(
                            this_parse_error[0], this_parse_error[1]
                        )
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


@require_http_methods(["POST", "GET"])
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
                                this_parse_error = parse_error(error)
                                if this_parse_error[0] is None:
                                    password_set_form.add_error(
                                        None, this_parse_error[1]
                                    )
                                else:
                                    password_set_form.add_error(
                                        this_parse_error[0], this_parse_error[1]
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

    job_choices = {**dict(JOB_CHOICES[1:]), **dict(HEALTH_CHOICES)}

    postcode_raw = user["ProductRegistrationVar9"]
    postcode = postcode_raw.split("|")[0] if "|" in postcode_raw else postcode_raw

    job_title_raw = (
        user.get("ContactVar2")
        if user.get("ContactVar2")
        else user["ProductRegistrationVar4"]
    )
    job_title = job_choices.get(job_title_raw)

    context = {
        "first_name": user["FirstName"],
        "last_name": user["LastName"],
        "email_address": user["EmailAddress"],
        "organisation": user["ProductRegistrationVar3"],
        "job_title": job_title,
        "postcode": postcode,
        "user_type": user["ProductRegistrationVar1"],
    }

    return render(request, "users/account.html", context)


@method_decorator(paragon_user_logged_in, name="dispatch")
class NewslettersView(View):
    paragon_client = Client()

    def get(self, request):
        client_user = self.paragon_client.get_user_profile(
            request.session.get("ParagonUser") or request.session.get("registration")
        )["content"]

        newsletters = deserialise(client_user["ProductRegistrationVar7"])

        if FeatureFlags.for_request(request).sz_email_year_groups == False:
            newsletters = map_school_years_to_primary_and_secondary(newsletters)

        newsletter_form = NewsLetterPreferencesForm(initial=newsletters)

        return self.render_preferences(request, newsletter_form)

    def post(self, request):
        newsletter_form = NewsLetterPreferencesForm(request.POST)
        if newsletter_form.is_valid():
            newsletters_form = dict(newsletter_form.cleaned_data)

            if FeatureFlags.for_request(request).sz_email_year_groups == False:
                newsletters_form = map_primary_and_secondary_to_school_years(
                    newsletters_form
                )

            serialised_newsletters = serialise(newsletters_form)

            try:
                self.paragon_client.update_user_profile(
                    user_token=request.session.get("ParagonUser")
                    or request.session.get("registration"),
                    subscriptions=serialised_newsletters,
                )

                # If school zone year groups is disabled, remove the specific years
                if FeatureFlags.for_request(request).sz_email_year_groups == False:
                    for k in school_year_groups:
                        del newsletters_form[k]

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

                return self.render_confirmation(request, newsletters_cleaned)
            except ParagonClientError as PCE:
                for error in PCE.args:
                    this_parse_error = parse_error(error)
                    if this_parse_error[0] is None:
                        newsletter_form.add_error(None, this_parse_error[1])
                    else:
                        newsletter_form.add_error(
                            this_parse_error[0], this_parse_error[1]
                        )
            return self.render_preferences(request, newsletter_form)

    def render_confirmation(self, request, newsletters_cleaned):
        return render(
            request,
            "users/confirmation_newsletters.html",
            {"preferences": newsletters_cleaned},
        )

    def render_preferences(self, request, newsletter_form):
        return render(
            request,
            "users/newsletter_preferences.html",
            {
                "form": newsletter_form,
                "schoolzone": FeatureFlags.for_request(request).sz_email_variant,
                "schoolzone_data_group": (
                    "schoolzone-year-groups"
                    if FeatureFlags.for_request(request).sz_email_year_groups
                    else "schoolzone"
                ),
            },
        )


class NewsletterRegisteringView(NewslettersView):
    # Override the dispatch method for registration decorator
    @method_decorator(paragon_user_registering)
    def dispatch(self, *args, **kwargs):
        return super(NewslettersView, self).dispatch(*args, **kwargs)

    def render_confirmation(self, request, newsletters_cleaned):
        # Delete the registaion session variable
        del request.session["registration"]
        return render(
            request,
            "users/confirmation_registration.html",
            {"email": settings.PHE_PARTNERSHIPS_EMAIL},
        )

    def render_preferences(self, request, newsletter_form):
        return render(
            request,
            "users/newsletter_preferences_registration.html",
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
        {"data": data, "sort": sort},
        # We pass the sort back into the template to ensure the current sort option is the default on page load
    )
