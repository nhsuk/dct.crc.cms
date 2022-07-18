from django.shortcuts import render
from campaignresourcecentre.campaigns.models import CampaignHubPage as campaign


def render_topic(request):
    campaigns = campaign.from_azure_search("", request)
    return render(
        request,
        "molecules/campaigns/campaigns.html",
        {"request": request, "campaigns": campaigns},
    )
