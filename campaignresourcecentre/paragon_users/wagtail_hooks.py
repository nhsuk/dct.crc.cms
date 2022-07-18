from django.urls import include, path, reverse
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from . import admin_urls


class ParagonUsersMenuItem(MenuItem):
    def is_shown(self, request):
        management_perms = [
            "paragon_users.manage_paragon_users",
            "paragon_users.manage_paragon_users_all_fields",
        ]
        return any(request.user.has_perm(perm) for perm in management_perms)


@hooks.register("register_admin_menu_item")
def register_menu_item():
    return ParagonUsersMenuItem(
        _("CRC Users"), reverse("paragon_users:index"), icon_name="user", order=400
    )


@hooks.register("register_permissions")
def register_permissions():
    return Permission.objects.filter(content_type__app_label="paragon_users")


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("paragon_users/", include(admin_urls, namespace="paragon_users")),
    ]
