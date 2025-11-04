from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem

from .views import CampaignResourceAuditReportView


@hooks.register("register_admin_urls")
def register_report_urls():
    """Register the report URL in Wagtail admin."""
    return [
        path(
            "reports/campaign-resource-audit/",
            CampaignResourceAuditReportView.as_view(),
            name="campaign_resource_audit_report",
        ),
        path(
            "reports/campaign-resource-audit/results/",
            CampaignResourceAuditReportView.as_view(results_only=True),
            name="campaign_resource_audit_report_results",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_report_menu_item():
    """Add the report to the Reports menu in Wagtail admin."""
    return AdminOnlyMenuItem(
        _("Campaign Resource Audit"),
        reverse("campaign_resource_audit_report"),
        icon_name="doc-full-inverse",
    )
