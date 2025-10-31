import csv
from datetime import datetime
from io import StringIO

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.reports import ReportView

from campaignresourcecentre.resources.models import ResourcePage


class CampaignResourceAuditReportView(ReportView):
    template_name = "reports/campaign_resource_audit.html"
    title = _("Campaign Resource Audit")
    header_icon = "doc-full-inverse"
    paginate_by = 25

    def get_queryset(self):
        queryset = ResourcePage.objects.all()
        ordering = self.request.GET.get("ordering", "title")
        return queryset.order_by(ordering)

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("export") == "csv":
            return self._generate_csv_export()
        return super().dispatch(request, *args, **kwargs)

    def _generate_csv_export(self):
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Type", "Campaign", "Title", "Slug", "Tags"])

        for resource in ResourcePage.objects.all().order_by("title"):
            writer.writerow(
                [
                    "Resource",
                    resource.get_parent().title,
                    resource.title,
                    resource.slug,
                    resource.parsed_tags,
                ]
            )

        today = datetime.now().strftime("%d-%m-%Y")
        filename = f"campaign_resource_report_{today}.csv"
        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
