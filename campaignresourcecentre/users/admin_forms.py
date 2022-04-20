from django.conf import settings
from django.urls import reverse

from wagtail.admin.forms.auth import PasswordResetForm as WagtailPasswordResetForm

from campaignresourcecentre.notifications import gov_notify_factory


class PasswordResetForm(WagtailPasswordResetForm):
    """Overridden to integrate with the GOV.UK Notify service."""

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a GOV.UK Notify reset password notification to `to_email`.
        """
        # Create reset link as per:
        # https://github.com/wagtail/wagtail/blob/v2.12/wagtail/admin/templates/wagtailadmin/account/password_reset/email.txt
        domain = getattr(
            settings, "BASE_URL", f"{context['protocol']}://{context['domain']}"
        )
        path = reverse(
            "wagtailadmin_password_reset_confirm",
            args=(context["uid"], context["token"]),
        )
        reset_link = domain + path

        notifications = gov_notify_factory()
        notifications.reset_password(to_email, context["user"].first_name, reset_link)
