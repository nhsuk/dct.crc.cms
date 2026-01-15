from wagtail.models import Page
from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage


def get_taggable_queryset(exclude_page_id=None):
    queryset = Page.objects.type(CampaignPage, ResourcePage).all()
    if exclude_page_id:
        queryset = queryset.exclude(id=exclude_page_id)

    return queryset
