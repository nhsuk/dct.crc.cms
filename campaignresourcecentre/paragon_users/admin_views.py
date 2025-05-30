from dataclasses import asdict
from math import ceil

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from wagtail.admin import messages
from wagtail.admin.auth import any_permission_required
from wagtail.admin.forms.search import SearchForm

from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.data_classes import user_from_dict
from campaignresourcecentre.paragon.exceptions import (
    ParagonClientError,
    ParagonClientTimeout,
)

from .forms import UserAdminForm, AdminPasswordSetForm
from .helpers.UsersPaginationWrapper import UsersPaginationWrapper as UsersWrapper


@any_permission_required(
    "paragon_users.manage_paragon_users",
    "paragon_users.manage_paragon_users_all_fields",
)
@require_http_methods(["GET"])
def index(request):
    return TemplateResponse(
        request,
        "paragon_users/index.html",
        {
            "query": request.GET.get("q", ""),
            "limit": request.GET.get("limit", 20),
            "page": request.GET.get("p", 1),
        },
    )


def search_users(request):
    search_string = ""
    error_message = ""

    paragon_client = Client()

    if "q" in request.GET:
        form = SearchForm(request.GET, placeholder=_("Email, first name & last name"))
        if form.is_valid():
            search_string = form.cleaned_data["q"]
    else:
        form = SearchForm(placeholder=_("Email, first name & last name"))

    users_per_page = int(request.GET.get("limit", 20))
    page_num = int(request.GET.get("p", 1))
    offset = (page_num - 1) * users_per_page

    try:
        response = paragon_client.search_users(
            string=search_string, offset=offset, limit=users_per_page
        )
        users = [user_from_dict(user_dict) for user_dict in response["content"]]
        users.sort(key=lambda user: user.created_at, reverse=True)

    except ParagonClientTimeout:
        users = []
        error_message = "The request to the service took too long to respond."

    except ParagonClientError as PCE:
        users = []
        if PCE.args[0] != "No records match the criteria":
            error_message = "Error: Fetching data from api failed"
        else:
            error_message = "Error: No users found for search: " + search_string

    #  Added this hack since we cant get access to the total number of users from DCX api.
    num_pages = page_num + 1 if len(users) >= users_per_page else page_num

    # Wrap users list to provide pagination attributes
    users = UsersWrapper(users, num_pages, page_num)

    return TemplateResponse(
        request,
        "paragon_users/results.html",
        {
            "users": users,
            "query_string": search_string,
            "error_message": error_message,
        },
    )


@any_permission_required(
    "paragon_users.manage_paragon_users",
    "paragon_users.manage_paragon_users_all_fields",
)
@require_http_methods(["POST", "GET"])
def edit(request, user_token):
    paragon_error = False
    form = None

    paragon_client = Client()

    try:
        response = paragon_client.get_user_profile(user_token=user_token)
        user = user_from_dict(response["content"])
    except ParagonClientError as PCE:
        user = None
        if PCE.args[0] != "Contact not found":
            paragon_error = True

    if user:
        all_fields_editable = request.user.has_perm(
            "paragon_users.manage_paragon_users_all_fields"
        )

        if request.method == "POST":
            form = UserAdminForm(
                request.POST,
                initial=asdict(user),
                all_fields_editable=all_fields_editable,
            )
            if form.is_valid():
                user.role = form.cleaned_data["role"]
                if all_fields_editable:
                    user.email = form.cleaned_data["email"]
                    user.first_name = form.cleaned_data["first_name"]
                    user.last_name = form.cleaned_data["last_name"]
                    user.organisation = form.cleaned_data["organisation"]
                    if form.cleaned_data["job_title"] == "health":
                        user.job_title = form.cleaned_data["area_work"]
                    else:
                        user.job_title = form.cleaned_data["job_title"]
                    user.postcode = form.cleaned_data["postcode"]

                try:
                    paragon_client.update_user_profile(
                        user.user_token,
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        organisation=user.organisation,
                        job_title=user.job_title,
                        role=user.role,
                        postcode=user.postcode,
                    )

                    messages.success(
                        request,
                        _(f"User '{user.full_name}' updated"),
                        buttons=[
                            messages.button(
                                reverse("paragon_users:edit", args=(user.user_token,)),
                                _("Edit"),
                            )
                        ],
                    )
                    return redirect("paragon_users:index")
                except ParagonClientError as PCE:
                    messages.error(request, _("Error saving the user to Paragon."))

            else:
                messages.error(request, _("The user could not be saved due to errors."))
        else:
            form = UserAdminForm(
                initial=asdict(user), all_fields_editable=all_fields_editable
            )

    return TemplateResponse(
        request,
        "paragon_users/edit.html",
        {"user": user, "paragon_error": paragon_error, "form": form},
    )


@any_permission_required(
    "paragon_users.manage_paragon_users",
    "paragon_users.manage_paragon_users_all_fields",
)
@require_http_methods(["GET", "POST"])
def set_password(request, user_token):
    paragon_error = False
    form = None
    paragon_client = Client()

    try:
        response = paragon_client.get_user_profile(user_token=user_token)
        user = user_from_dict(response["content"])
    except ParagonClientError as PCE:
        user = None
        if PCE.args[0] != "Contact not found":
            paragon_error = True

    if request.method == "POST":
        form = AdminPasswordSetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            try:
                paragon_client.update_password(user_token=user_token, password=password)

                messages.success(
                    request,
                    _(f"User '{user.full_name}' password updated"),
                    buttons=[
                        messages.button(
                            reverse(
                                "paragon_users:set_password", args=(user.user_token,)
                            ),
                            _("Set password"),
                        )
                    ],
                )
                return redirect("paragon_users:index")
            except ParagonClientError as PCE:
                messages.error(request, _("Error updating user password."))

        else:
            messages.error(
                request, _("The password could not be updated due to errors.")
            )
    else:
        form = AdminPasswordSetForm()

    return TemplateResponse(
        request,
        "paragon_users/set_password.html",
        {"user": user, "paragon_error": paragon_error, "form": AdminPasswordSetForm},
    )
