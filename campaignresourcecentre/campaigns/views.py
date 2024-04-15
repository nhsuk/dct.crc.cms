from django.shortcuts import render
from campaignresourcecentre.campaigns.models import CampaignHubPage as campaign
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
