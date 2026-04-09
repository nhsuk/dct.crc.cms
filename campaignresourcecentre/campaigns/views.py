from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from wagtail_modeladmin.views import DeleteView

from campaignresourcecentre.campaigns.models import (
    CampaignHubPage as campaign,
    pages_with_topic,
)
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

    def get_template_names(self):
        return ["campaigns/delete_topic.html"]

    def confirmation_message(self):
        campaign_pages, resource_pages = pages_with_topic(self.instance.code)
        campaigns, resources = len(campaign_pages), len(resource_pages)
        if campaigns or resources:
            return _(
                "This topic is tagged on %(campaigns)d campaign page(s) "
                "and %(resources)d resource page(s). Please remove the "
                "topic from those pages before deleting it."
            ) % {"campaigns": campaigns, "resources": resources}
        return _(
            "%(campaigns)d campaign page(s) and %(resources)d resource "
            "page(s) have this tag. Are you sure you want to delete this "
            "%(verbose_name)s?"
        ) % {
            "campaigns": campaigns,
            "resources": resources,
            "verbose_name": self.verbose_name,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign_pages, resource_pages = pages_with_topic(self.instance.code)
        tagged_pages = [
            {
                "page": p,
                "page_type": "Campaign",
            }
            for p in campaign_pages
        ] + [
            {
                "page": p,
                "page_type": "Resource",
            }
            for p in resource_pages
        ]
        context["tagged_pages"] = tagged_pages
        return context

    def post(self, request, *args, **kwargs):
        campaign_pages, resource_pages = pages_with_topic(self.instance.code)
        campaigns, resources = len(campaign_pages), len(resource_pages)
        if campaigns or resources:
            messages.error(
                request,
                _(
                    "Cannot delete this topic. It is still tagged on "
                    "%(campaigns)d campaign page(s) and %(resources)d "
                    "resource page(s). Please remove the topic from "
                    "those pages first."
                )
                % {"campaigns": campaigns, "resources": resources},
            )
            return redirect(self.index_url)
        return super().post(request, *args, **kwargs)
