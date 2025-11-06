import django_filters
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import ReportView

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from campaignresourcecentre.core.templatetags.json_lookup import data as taxonomy_data


def get_all_taxonomy_terms():
    """Get all taxonomy terms as choices for filtering."""
    choices = []
    for category in taxonomy_data:
        for item in category["children"]:
            choices.append((item["code"], item["label"]))

    return sorted(choices, key=lambda x: x[1])


class CampaignResourceFilterSet(WagtailFilterSet):
    campaign = django_filters.ModelMultipleChoiceFilter(
        label="Campaign",
        queryset=CampaignPage.objects.live().order_by("title"),
        widget=CheckboxSelectMultiple,
        method="filter_campaign",
    )

    taxonomy = django_filters.MultipleChoiceFilter(
        label="Taxonomy",
        choices=get_all_taxonomy_terms,
        widget=CheckboxSelectMultiple,
        method="filter_taxonomy",
    )

    class Meta:
        model = ResourcePage
        fields = ["campaign", "taxonomy"]

    def filter_campaign(self, queryset, name, value):
        """Filter resources that are children of the selected campaigns."""
        if not value:
            return queryset

        for campaign in value:
            filtered = queryset.descendant_of(campaign)
        return filtered

    def filter_taxonomy(self, queryset, name, value):
        """Filter resources by taxonomy terms."""
        if not value:
            return queryset

        matching_ids = []
        for resource in queryset:
            terms = resource.taxonomy
            codes = [term["code"] for term in terms]

            if all(selected_code in codes for selected_code in value):
                matching_ids.append(resource.id)

        filtered = queryset.filter(id__in=matching_ids)
        return filtered


class CampaignResourceAuditReportView(ReportView):
    index_url_name = "campaign_resource_audit_report"
    index_results_url_name = "campaign_resource_audit_report_results"
    template_name = "reports/campaign_resource_audit.html"
    results_template_name = "reports/campaign_resource_audit_results.html"
    page_title = _("Campaign Resource Audit")
    header_icon = "doc-full-inverse"
    paginate_by = 50
    filterset_class = CampaignResourceFilterSet

    export_headings = {
        "objecttype": "Type",
        "parent_campaign_chain": "Campaign Hierarchy",
        "title": "Title",
        "admin_url": "Wagtail URL",
        "topics": "Topics",
        "target_audience": "Target Audience",
        "language": "Language",
        "profession": "Profession",
        "alternative_format": "Alternative Format",
        "taxonomy_resource_type": "Resource Type",
        "first_published_date": "First Published",
        "last_published_date": "Last Published",
        "publish_status": "Status",
    }

    list_export = list(export_headings.keys())

    def get_queryset(self):
        return ResourcePage.objects.all()
