from django.shortcuts import render
from campaignresourcecentre.campaigns.models import CampaignHubPage as campaign
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def render_topic(request):
    campaign_hub_page = campaign.objects.first()

    if request.GET.get("sort") == "recommended":
        campaigns = campaign_hub_page.from_database(request)
    else:
        campaigns = campaign_hub_page.from_azure_search(request)

    return render(
        request,
        "molecules/campaigns/campaigns.html",
        {"request": request, "campaigns": campaigns},
    )
