from django.shortcuts import render
from django.utils.translation import gettext as _
from wagtail_modeladmin.views import DeleteView

from campaignresourcecentre.campaigns.models import (
    CampaignHubPage as campaign,
    CampaignPage,
)
from campaignresourcecentre.resources.models import ResourcePage
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def render_topic(request):
    campaign_hub_page = campaign.objects.first()
    context = campaign_hub_page.get_context(request)

    return render(
        request,
        "molecules/campaigns/campaigns.html",
        context,
    )


class TopicDeleteView(DeleteView):
    """Custom delete confirmation that shows how many pages are affected."""

    def confirmation_message(self):
        contains_code = {"taxonomy_json__contains": f'"code":"{self.instance.code}"'}
        campaigns = CampaignPage.objects.filter(**contains_code).count()
        resources = ResourcePage.objects.filter(**contains_code).count()
        if campaigns or resources:
            return _(
                "This topic is tagged on %(campaigns)d campaign page(s) "
                "and %(resources)d resource page(s). Deleting it will "
                "remove the tag from all of them."
            ) % {"campaigns": campaigns, "resources": resources}
        return _("Are you sure you want to delete this %s?") % self.verbose_name
