from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from campaignresourcecentre.campaigns.models import CampaignUpdateBase
from campaignresourcecentre.utils.models import BasePage

from campaignresourcecentre.campaigns.blocks import HomePageBlocks
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images import get_image_model_string


class HomePage(BasePage):
    max_count = 1
    template = "home_page.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    introduction = RichTextField(features=["bold", "italic"])
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_align = models.CharField(
        max_length=15,
        choices=(("left", "Left"), ("center", "Center"), ("right", "Right")),
        default="right",
    )
    campaign_updates_heading = models.CharField(
        blank=True,
        max_length=75,
        default="Latest updates",
        verbose_name="Heading",
        help_text="This is only shown if there are campaign updates to display.",
    )
    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    body = StreamField((HomePageBlocks(required=False)))

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("introduction"),
                ImageChooserPanel("hero_image"),
                FieldPanel("hero_align"),
            ],
            heading="Introduction",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("campaign_updates_heading"),
                InlinePanel(
                    "campaign_updates", heading="Updates", label="Update", max_num=3
                ),
            ],
            heading="Campaign Updates",
        ),
        SnippetChooserPanel("call_to_action"),
        StreamFieldPanel("body"),
    ]

    def get_campaign_updates(self):
        """Get the campaign updates for display in the template.
        Uses `select_related()) to fetch foreign key objects in the same
        query."""

        return [
            {
                "link_text": update.get_link_text(),
                "description": update.description,
                "image": update.image,
                "url": update.get_link_url(),
            }
            for update in self.campaign_updates.select_related("link_page", "image")
        ]

    def get_context(self, request, *args, **kwargs):
        """Adds data to the template context for display on the page."""
        context = super().get_context(request, *args, **kwargs)
        context.update(campaign_updates=self.get_campaign_updates())
        return context


class CampaignUpdate(CampaignUpdateBase):
    page = ParentalKey(HomePage, related_name="campaign_updates")
