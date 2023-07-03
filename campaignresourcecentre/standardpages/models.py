from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.images import get_image_model_string

from campaignresourcecentre.utils.blocks import StoryBlock
from campaignresourcecentre.utils.models import BasePage, RelatedPage
from campaignresourcecentre.campaigns.blocks import AboutPageSection


class InformationPageRelatedPage(RelatedPage):
    source_page = ParentalKey("InformationPage", related_name="related_pages")


class InformationPage(BasePage):
    template = "information_page.html"

    introduction = models.TextField(blank=True)

    body = StreamField(StoryBlock(required=False), blank=True, use_json_field=True)
    section = StreamField(
        AboutPageSection(required=False), blank=True, use_json_field=True
    )

    search_fields = BasePage.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("section"),
    ]


class AboutPage(InformationPage):
    template = "about_page.html"

    description = RichTextField(
        features=["bold", "italic", "link", "h2", "h3", "ol", "ul"],
        help_text="Introduction section for the resource page",
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

    content_panels = BasePage.content_panels + [
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("summary"),
                FieldPanel("description"),
                FieldPanel("image"),
                FieldPanel("image_alt_text"),
            ],
            heading="Page Hero",
        ),
        FieldPanel("body"),
        FieldPanel("section"),
    ]


class IndexPage(BasePage):
    template = "index_page.html"

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [FieldPanel("introduction")]

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
