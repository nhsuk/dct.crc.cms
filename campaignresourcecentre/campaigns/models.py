import json
from datetime import datetime
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from html import unescape
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailreacttaxonomy.edit_handlers import TaxonomyPanel
from wagtailreacttaxonomy.models import TaxonomyMixin
from wagtailreacttaxonomy.models import TaxonomyTerms

from campaignresourcecentre.page_lifecycle.forms import PageLifecycleForm
from campaignresourcecentre.page_lifecycle.models import PageLifecycleMixin
from campaignresourcecentre.resources.models import ResourcePage
from campaignresourcecentre.utils.models import BasePage, LinkFields
from campaignresourcecentre.core.templatetags.json_lookup import get_taxonomies

from .blocks import CampaignDetailsBlock, CampaignsPageBlocks, CommonBlocks
import logging


logger = logging.getLogger(__name__)


class Topic(models.Model):
    """Campaign topics. Managed in the Taxonomy section of the Wagtail admin,
    which itself is defined in `utils.wagtail_hooks.py`"""

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CampaignHubPage(BasePage):
    max_count = 1
    template = "campaign_hub.html"

    parent_page_types = ["home.HomePage"]
    subpage_types = ["campaigns.CampaignPage"]

    introduction = models.TextField(blank=True)
    campaign_updates_heading = models.CharField(
        blank=True,
        max_length=75,
        default="Latest campaign updates",
        verbose_name="Heading",
        help_text="This is only shown if there are campaign updates to display.",
    )
    campaign_updates_bg_colour = models.CharField(
        choices=[("app-section--white", "white"), ("app-section--grey", "nhs grey")],
        max_length=45,
        default="app-section--white",
        help_text="set background colour for the section",
    )

    body = StreamField(CampaignsPageBlocks(required=False), blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("campaign_updates_heading"),
                FieldPanel("campaign_updates_bg_colour"),
                InlinePanel(
                    "campaign_updates", heading="Updates", label="Update", max_num=1
                ),
            ],
            heading="Campaign Updates",
        ),
        MultiFieldPanel([StreamFieldPanel("body")], heading="Body"),
    ]

    promote_panels = promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("search_description"),
            ],
            "For search engines",
        )
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
                "image_alt_text": update.image_alt_text,
                "url": update.get_link_url(),
            }
            for update in self.campaign_updates.select_related("link_page", "image")
        ]

    def from_azure_search(self, request):
        from campaignresourcecentre.search.azure import AzureSearchBackend

        topic = request.GET.get("topic")
        sort = request.GET.get("sort") or "newest"
        search = AzureSearchBackend({})
        search_value = ""
        fields_queryset = {"objecttype": "campaign"}
        facets_queryset = {}
        results_per_page = "50"
        if topic and topic != "ALL":
            facets_queryset["TOPIC"] = topic
        sort_by = None
        if sort == "oldest":
            sort_by = "last_published_at"
        elif sort == "newest":
            sort_by = "last_published_at desc"
        response = search.azure_search(
            search_value, fields_queryset, facets_queryset, sort_by, results_per_page
        )
        campaigns = []
        try:
            if response["search_content"] and response["search_content"]["value"]:
                campaigns = response["search_content"]["value"]
        except KeyError as err:
            logger.error(err)

        return [
            {
                "title": campaign["content"]["resource"].get("title"),
                "summary": campaign["content"]["resource"].get("summary"),
                "image_url": campaign["content"]["resource"].get("image_url"),
                "image_alt": campaign["content"]["resource"].get("image_alt"),
                "listing_summary": campaign["content"]["resource"].get("descrition"),
                "url": campaign["content"]["resource"].get("object_url"),
            }
            for campaign in campaigns
        ]

    def from_database(self, request):
        # Get the initial queryset of child campaign pages of the hub.
        campaigns = (
            CampaignPage.objects.live()
            .public()
            .child_of(self)
            .order_by("-first_published_at")
        )

        # Apply filtering to the child pages, if applicable.
        topic = request.GET.get("topic")
        if topic:
            try:
                topic = int(topic)
            except ValueError:
                # topic should be an int, return nothing if the filter value in
                # the URL has been tampered with.
                campaigns = CampaignPage.objects.none()
            else:
                campaigns = campaigns.filter(topics=topic)

        # Format the campaigns for display in the template
        return [
            {
                "title": campaign.listing_title or campaign.title,
                "image": campaign.listing_image or campaign.image,
                "listing_summary": campaign.listing_summary,
                "url": campaign.url,
            }
            for campaign in campaigns
        ]

    def get_context(self, request, *args, **kwargs):
        from_azure_search = settings.CAMPAIGNS_FROM_AZ
        filter_codes = settings.CAMPAIGN_HUB_PAGE_FILTERS

        """Adds data to the template context for display on the page."""
        taxonomy_json = json.loads(
            TaxonomyTerms.objects.get(taxonomy_id="crc_taxonomy").terms_json
        )
        health_topics = next((x for x in taxonomy_json if x["code"] == "TOPIC"), None)[
            "children"
        ]
        topics_for_filter = [
            obj for obj in health_topics if obj["code"] in filter_codes
        ]

        selected_topic = request.GET.get("topic") or "ALL"
        sort = request.GET.get("sort") or "newest"

        if from_azure_search:
            campaigns = self.from_azure_search(request)
        else:
            campaigns = self.from_database(request)

        # Pagination
        page = request.GET.get("page", 1)
        paginator = Paginator(campaigns, settings.DEFAULT_PER_PAGE)
        try:
            campaigns = paginator.page(page)
        except PageNotAnInteger:
            campaigns = paginator.page(1)
        except EmptyPage:
            campaigns = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            campaign_updates=self.get_campaign_updates(),
            selected_topic=selected_topic,
            sort=sort,
            campaigns=campaigns,
            topics=topics_for_filter,
        )
        return context


class CampaignUpdateBase(LinkFields, Orderable):
    """Campaign updates are separate models of which mutliple ones can be "
    "added to the page using `InlinePanel`. Inherits from `utils.LinkFields`
    which provides page, url and link text fields."""

    page = None  # add to concrete inherited models
    image = models.ForeignKey(
        get_image_model_string(),
        related_name="+",
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose an image to display.",
    )
    description = models.TextField(help_text="Enter the text to display.")
    image_alt_text = models.TextField(
        blank=True,
        help_text="Leave blank if the image is purely decorative. Most images on CRC will not require alt text.",
    )

    class Meta:
        abstract = True

    def clean(self):
        # TODO: Change validation so errors aren't raised one at a time. This
        # can be done using a `defaultdict` and passing that to `ValidationError`.
        # apply parent validation first
        super().clean()
        if self.link_url and not self.image:
            raise ValidationError(
                {
                    "image": ValidationError(
                        "Please select an image to display for the external URL."
                    )
                }
            )
        if self.link_url and not self.description:
            raise ValidationError(
                {
                    "description": ValidationError(
                        "Please enter the description text for the external URL."
                    )
                }
            )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("image"),
                FieldPanel("description"),
                FieldPanel("image_alt_text"),
                PageChooserPanel("link_page", "campaigns.CampaignPage"),
                FieldPanel("link_url"),
                FieldPanel("link_text"),
            ],
            "Update",
        )
    ]


class CampaignUpdate(CampaignUpdateBase):
    page = ParentalKey(CampaignHubPage, related_name="campaign_updates")


class CampaignPage(PageLifecycleMixin, TaxonomyMixin, BasePage):
    TAXONOMY_TERMS_ID = "crc_taxonomy"

    template = "campaign_page.html"

    parent_page_types = ["campaigns.CampaignHubPage", "campaigns.CampaignPage"]
    subpage_types = ["campaigns.CampaignPage", "resources.ResourcePage"]

    base_form_class = PageLifecycleForm

    # Max length is set to 480 using clean() method below.
    description = RichTextField(
        features=["bold", "italic", "link", "h2", "h3", "ol", "ul"],
        help_text="Introduction section for the campaign page. This is limited to 480 characters to make sure the page loads properly on frontend. Please preview the page before you publish as this depends on length of the below image and may alter the page overall design.",
    )
    summary = RichTextField(
        features=["bold", "italic", "link", "h2", "h3", "ol", "ul"],
        help_text="Short line of text for display on the campaign page",
    )
    image = models.ForeignKey(
        get_image_model_string(), null=True, related_name="+", on_delete=models.SET_NULL
    )
    image_alt_text = models.TextField(
        blank=True,
        help_text="Leave blank if the image is purely decorative. Most images on CRC will not require alt text.",
    )
    related_website = models.URLField(blank=True, help_text="Enter a URL to link to.")
    related_website_text = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the text for the link. This is required for external "
        "URLs. If an internal page is chosen and this field is blank the page "
        "title will be shown",
    )
    details = StreamField(CampaignDetailsBlock(required=False), blank=True)
    topics = ParentalManyToManyField(Topic, blank=True)
    body = StreamField(CampaignsPageBlocks(required=False), blank=True)

    def search_indexable(self):
        return CampaignHubPage.objects.all()[0].id == self.get_parent().id

    def objecttype(self):
        return "campaign"

    def get_sub_campaigns(self):
        """Get the sub-campaigns (child pages of the campaign) for display in
        the template."""
        sub_campaigns = (
            CampaignPage.objects.child_of(self)
            .live()
            .public()
            .select_related("image", "listing_image")
        )
        return [
            {
                "title": p.title,
                "summary": p.summary,
                "image": p.listing_image if p.listing_image else p.image,
                "image_alt_text": p.image_alt_text,
                "url": p.url,
            }
            for p in sub_campaigns
        ]

    def get_resources(self, user_role):
        """Get the child resource pages for display in the template."""
        resources = (
            ResourcePage.objects.child_of(self)
            .live()
            .public()
            .select_related("listing_image", "listing_image")
        )
        resources_list = []
        for resource in resources:
            resource_items = resource.resource_items.select_related("image")
            resource_item = resource_items[0] if (len(resource_items) > 0) else None
            resources_list.append(
                {
                    "title": resource.title,
                    "description": resource.description,
                    "summary": resource.summary,
                    "image": resource_item.image if resource_item else None,
                    "image_alt_text": resource_item.image_alt_text
                    if resource_item
                    else None,
                    "url": resource.url,
                    "last_published_at": resource.last_published_at,
                }
            )
        return resources_list

    def get_az_item(self):
        return {
            "objecttype": self.objecttype(),
            "object_url": f"{self.url}",
            "title": self.title,
            "description": self.description,
            "summary": self.summary,
            "taxonomy_json": self.taxonomy_json,
            "last_published_at": datetime.timestamp(self.last_published_at),
            "image_url": self.image and self.image.get_rendition("width-400").url,
            "image_alt": self.image and self.image_alt_text,
            "code": self.slug,
        }

    def get_context(self, request, *args, **kwargs):
        """Adds data to the template context for display on the page."""
        json_data = {}
        if self.taxonomy_json:
            json_data = json.loads(self.taxonomy_json)
        context = super().get_context(request, *args, **kwargs)
        user_role = (
            request.session.get("UserDetails")
            and request.session.get("UserDetails")["ProductRegistrationVar1"]
        )
        context.update(
            details=self.details,
            sub_campaigns=self.get_sub_campaigns(),
            resources=self.get_resources(user_role),
            taxonomy_json=json_data,
            topics_present=get_taxonomies(json_data, "TOPIC"),
            targaud_present=get_taxonomies(json_data, "TARGAUD"),
        )
        return context

    content_panels = BasePage.content_panels + [
        FieldPanel(
            "topics", heading="Campaign Topics", widget=forms.CheckboxSelectMultiple
        ),
        MultiFieldPanel(
            [
                FieldPanel("summary"),
                FieldPanel("description"),
                ImageChooserPanel("image"),
                FieldPanel("image_alt_text"),
            ],
            heading="Page Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("related_website"),
                FieldPanel("related_website_text"),
                StreamFieldPanel("details"),
            ],
            heading="Campaign Details",
            classname="collapsible",
        ),
        MultiFieldPanel([StreamFieldPanel("body")], heading="Body"),
    ]

    taxonomy_term_panels = [
        TaxonomyPanel("taxonomy_json", taxonomy_terms_id=TAXONOMY_TERMS_ID)
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(taxonomy_term_panels, heading="Taxonomy"),
            ObjectList(BasePage.promote_panels, heading="Promote"),
            ObjectList(
                BasePage.settings_panels + PageLifecycleMixin.panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    def clean(self):
        description_len = len(unescape(strip_tags(self.description)))
        if description_len > 480:
            raise ValidationError(
                {
                    "description": f"The description cannot be longer than 480 characters. You have {description_len} characters."
                }
            )
