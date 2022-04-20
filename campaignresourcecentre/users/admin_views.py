from wagtail.admin.views.account import PasswordResetView as WagtailPasswordResetView

from .admin_forms import PasswordResetForm


class PasswordResetView(WagtailPasswordResetView):
    form_class = PasswordResetForm
