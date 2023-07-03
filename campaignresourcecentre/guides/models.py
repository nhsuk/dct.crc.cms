from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.search import index
from wagtail.blocks import ChoiceBlock

from campaignresourcecentre.campaigns.blocks import CommonBlocks, GuidePageBlocks
from campaignresourcecentre.utils.models import BasePage


class GuidePage(BasePage):
    template = "guide_page.html"

    parent_page_types = ["GuideHubPage"]
    subpage_types = []

    introduction = models.TextField(blank=True)

    summary = RichTextField(
        features=["bold", "italic", "link", "h2", "h3", "ol", "ul"],
        default="",
        help_text="Summary section for the Guides page",
    )

    background_colour = models.CharField(
        choices=[("app-section--white", "white"), ("app-section--grey", "nhs grey")],
        max_length=45,
        default="app-section--white",
        help_text="set background colour for the section",
    )

    image = models.ForeignKey(
        get_image_model_string(), null=True, related_name="+", on_delete=models.SET_NULL
    )

    image_alt_text = models.TextField(
        blank=True,
        help_text="Leave blank if the image is purely decorative. Most images on CRC will not require alt text.",
    )

    body = StreamField(GuidePageBlocks())

    search_fields = BasePage.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("summary"),
                FieldPanel("image"),
                FieldPanel("image_alt_text"),
                FieldPanel("background_colour"),
            ],
            heading="Page Hero",
        ),
        FieldPanel("body"),
    ]


class GuideHubPage(BasePage):
    template = "guide_hub_page.html"

    parent_page_types = ["home.HomePage"]
    subpage_types = ["GuidePage"]

    introduction = models.TextField(blank=True)

    body = StreamField(CommonBlocks(required=False), blank=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        subpages = self.get_children().live()
        per_page = settings.DEFAULT_PER_PAGE
        page_number = request.GET.get("page")
        paginator = Paginator(subpages, per_page)

        try:
            subpages = paginator.page(page_number)
        except PageNotAnInteger:
            subpages = paginator.page(1)
        except EmptyPage:
            subpages = paginator.page(paginator.num_pages)

        context["subpages"] = subpages

        return context
