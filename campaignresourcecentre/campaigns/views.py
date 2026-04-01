from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from wagtail_modeladmin.views import DeleteView

from campaignresourcecentre.campaigns.models import (
    CampaignHubPage as campaign,
    count_pages_with_topic,
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

    def confirmation_message(self):
        campaigns, resources = count_pages_with_topic(self.instance.code)
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

    def post(self, request, *args, **kwargs):
        campaigns, resources = count_pages_with_topic(self.instance.code)
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
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            if "Please select at least one topic tag" in str(e):
                messages.error(
                    request,
                    _(
                        "Cannot delete this topic. Some pages would be left with "
                        "no topic tags. Please reassign their topics first."
                    ),
                )
                return redirect(self.index_url)
            raise
