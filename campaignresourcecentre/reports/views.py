import django_filters
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import ReportView

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage


class CampaignResourceFilterSet(WagtailFilterSet):
    campaign = django_filters.ModelMultipleChoiceFilter(
        label="Campaign",
        queryset=CampaignPage.objects.live().order_by("title"),
        widget=CheckboxSelectMultiple,
        method="filter_campaign",
    )

    class Meta:
        model = ResourcePage
        fields = ["campaign"]

    def filter_campaign(self, queryset, name, value):
        if not value:
            return queryset
        filtered = ResourcePage.objects.none()
        for campaign in value:
            filtered |= queryset.child_of(campaign)
        return filtered


class CampaignResourceAuditReportView(ReportView):
    index_url_name = "campaign_resource_audit_report"
    index_results_url_name = "campaign_resource_audit_report_results"
    template_name = "reports/campaign_resource_audit.html"
    results_template_name = "reports/campaign_resource_audit_results.html"
    page_title = _("Campaign Resource Audit")
    header_icon = "doc-full-inverse"
    paginate_by = 25
    filterset_class = CampaignResourceFilterSet

    list_export = ["resource_type", "campaign_name", "title", "slug", "parsed_tags"]
    export_headings = {
        "resource_type": "Type",
        "campaign_name": "Campaign",
        "title": "Title",
        "slug": "Slug",
        "parsed_tags": "Tags",
    }

    def get_queryset(self):
        return ResourcePage.objects.all()
