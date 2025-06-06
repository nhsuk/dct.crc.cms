from django.core.exceptions import ValidationError
from django.db import models
from django.utils.decorators import method_decorator
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    HelpPanel,
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.images import get_image_model_string
from wagtail.snippets.models import register_snippet

from campaignresourcecentre.utils.cache import get_default_cache_control_decorator

SEARCH_DESCRIPTION_LABEL = "Meta description"  # NOTE changing this requires migrations


class LinkFields(models.Model):
    """
    Adds fields for internal and external links with some methods to simplify the rendering:

    <a href="{{ obj.get_link_url }}">{{ obj.get_link_text }}</a>
    """

    link_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_link_page",
        help_text="Choose a page to link to.",
    )
    link_url = models.URLField(blank=True, help_text="Enter a URL to link to.")
    link_text = models.CharField(
        blank=True,
        max_length=255,
        help_text="Enter the text for the link. This is required for external "
        "URLs. If an internal page is chosen and this field is blank the page "
        "title will be shown",
    )

    class Meta:
        abstract = True

    def clean(self):
        if not self.link_page and not self.link_url:
            raise ValidationError(
                {
                    "link_url": ValidationError(
                        "You must specify link page or link url."
                    ),
                    "link_page": ValidationError(
                        "You must specify link page or link url."
                    ),
                }
            )

        if self.link_page and self.link_url:
            raise ValidationError(
                {
                    "link_url": ValidationError(
                        "You must specify link page or link url. You can't use both."
                    ),
                    "link_page": ValidationError(
                        "You must specify link page or link url. You can't use both."
                    ),
                }
            )

        if not self.link_page and not self.link_text:
            raise ValidationError(
                {
                    "link_text": ValidationError(
                        "You must specify link text, if you use the link url field."
                    )
                }
            )

    def get_link_text(self):
        if self.link_text:
            return self.link_text

        if self.link_page:
            return self.link_page.title

        return ""

    def get_link_url(self):
        if self.link_page:
            return self.link_page.get_url

        return self.link_url

    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel("link_page"),
                FieldPanel("link_url"),
                FieldPanel("link_text"),
            ],
            "Link",
        )
    ]


# Related pages
class RelatedPage(Orderable, models.Model):
    page = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, related_name="+"
    )

    class Meta:
        abstract = True
        ordering = ["sort_order"]

    panels = [PageChooserPanel("page")]


# Generic social fields abstract class to add social image/text to any new content type easily.
class SocialFields(models.Model):
    social_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    social_text = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel(
            [FieldPanel("social_image"), FieldPanel("social_text")],
            "Social networks",
        )
    ]


# Generic listing fields abstract class to add listing image/text to any new content type easily.
class ListingFields(models.Model):
    listing_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose the image you wish to be displayed when this page appears in listings",
    )
    listing_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Override the page title used when this page appears in listings",
    )
    listing_summary = models.CharField(
        max_length=255,
        blank=True,
        help_text="The text summary used when this page appears in listings. It's also used as "
        f"the description for search engines if the '{SEARCH_DESCRIPTION_LABEL}' field above is not defined.",
    )

    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("listing_image"),
                FieldPanel("listing_title"),
                FieldPanel("listing_summary"),
            ],
            "Listing information",
        )
    ]


@register_snippet
class CallToActionSnippet(models.Model):
    title = models.CharField(max_length=255)
    summary = RichTextField(blank=True, max_length=255)
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    link = StreamField(
        blocks.StreamBlock(
            [
                (
                    "external_link",
                    blocks.StructBlock(
                        [("url", blocks.URLBlock()), ("title", blocks.CharBlock())],
                        icon="link",
                    ),
                ),
                (
                    "internal_link",
                    blocks.StructBlock(
                        [
                            ("page", blocks.PageChooserBlock()),
                            ("title", blocks.CharBlock(required=False)),
                        ],
                        icon="link",
                    ),
                ),
            ],
            max_num=1,
            required=True,
        ),
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("summary"),
        FieldPanel("link"),
    ]

    def get_link_text(self):
        # Link is required, so we should always have
        # an element with index 0
        block = self.link[0]

        title = block.value["title"]
        if block.block_type == "external_link":
            return title

        # Title is optional for internal_link
        # so fallback to page's title, if it's empty
        return title or block.value["page"].title

    def get_link_url(self):
        # Link is required, so we should always have
        # an element with index 0
        block = self.link[0]

        if block.block_type == "external_link":
            return block.value["url"]

        return block.value["page"].get_url()

    def __str__(self):
        return self.title


@register_setting
class SocialMediaSettings(BaseSiteSetting):
    twitter_handle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your Twitter username without the @, e.g. katyperry",
    )
    facebook_app_id = models.CharField(
        max_length=255, blank=True, help_text="Your Facebook app ID."
    )
    default_sharing_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Default sharing text to use if social text has not been set on a page.",
    )
    site_name = models.CharField(
        max_length=255,
        blank=True,
        default="Campaign Resource Centre",
        help_text="Site name, used by Open Graph.",
    )


@register_setting
class SystemMessagesSettings(BaseSiteSetting):
    class Meta:
        verbose_name = "system messages"

    title_404 = models.CharField("Title", max_length=255, default="Page not found")
    body_404 = RichTextField(
        "Text",
        default="<p>You may be trying to find a page that doesn&rsquo;t exist or has been moved.</p>",
    )

    banner_enabled = models.BooleanField("Enabled", default=False)
    green_banner = models.TextField("Green banner", default="", blank=True)
    red_banner = models.TextField("Red banner", default="", blank=True)

    panels = [
        MultiFieldPanel([FieldPanel("title_404"), FieldPanel("body_404")], "404 page"),
        MultiFieldPanel(
            [
                FieldPanel("banner_enabled"),
                FieldPanel("green_banner"),
                FieldPanel("red_banner"),
            ],
            "Admin Site Banner",
        ),
    ]


# Apply default cache headers on this page model's serve method.
@method_decorator(get_default_cache_control_decorator(), name="serve")
class BasePage(SocialFields, ListingFields, Page):
    show_in_menus_default = True

    class Meta:
        abstract = True
        permissions = [
            ("unpublish", "Can unpublish a published page"),
        ]

    def search_indexable(self):
        return False

    promote_panels = (
        Page.promote_panels + SocialFields.promote_panels + ListingFields.promote_panels
    )


BasePage._meta.get_field("seo_title").verbose_name = "Title tag"
BasePage._meta.get_field("search_description").verbose_name = SEARCH_DESCRIPTION_LABEL


@register_setting(icon="view")
class Tracking(BaseSiteSetting):
    google_tag_manager_id = models.CharField(
        max_length=255, blank="True", help_text="Your Google Tag Manager ID"
    )


@register_setting
class FeatureFlags(BaseSiteSetting):
    class Meta:
        verbose_name = "Feature flags"

    sz_email_variant = models.BooleanField(
        "School Zone email journey",
        default=False,
        help_text="Enable or disable the School Zone email signup journey variant",
    )

    sz_email_year_groups = models.BooleanField(
        "School Zone email year groups (requires School Zone email journey)",
        default=False,
        help_text="Enable or disable the School Zone email year groups feature flag",
    )

    panels = [
        HelpPanel(content="Custom feature flags which can be toggled on and off."),
        FieldPanel("sz_email_variant"),
        FieldPanel("sz_email_year_groups"),
    ]
