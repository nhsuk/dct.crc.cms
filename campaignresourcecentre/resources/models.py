from datetime import datetime
from collections import defaultdict
import json
from django.core.exceptions import ValidationError
from django.db import models
from urllib.parse import quote

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.documents import get_document_model_string
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from wagtailreacttaxonomy.edit_handlers import TaxonomyPanel
from wagtailreacttaxonomy.models import TaxonomyMixin

from campaignresourcecentre.page_lifecycle.forms import PageLifecycleForm
from campaignresourcecentre.page_lifecycle.models import PageLifecycleMixin
from campaignresourcecentre.utils.models import BasePage
from campaignresourcecentre.baskets.basket import Basket
from campaignresourcecentre.core.templatetags.json_lookup import get_taxonomies
from campaignresourcecentre.paragon_users.helpers.token_signing import sign


class ResourcePage(PageLifecycleMixin, TaxonomyMixin, BasePage):
    TAXONOMY_TERMS_ID = "crc_taxonomy"

    template = "resource_page.html"

    parent_page_types = ["campaigns.CampaignPage"]
    subpage_types = []

    base_form_class = PageLifecycleForm

    class PermissionRole(models.TextChoices):
        ALL = "all", "Open access"
        STANDARD = "standard", "Standard"
        UBER = "uber", "Uber"

    description = RichTextField(
        features=["bold", "italic", "h3", "h4", "ol", "ul", "link"],
        help_text="Introduction section for the campaign page",
    )
    summary = models.TextField(
        help_text="A short line of text for display on campaign hub. Maximum 125 character limit.",
        max_length=125,
    )
    permission_role = models.CharField(
        max_length=10, choices=PermissionRole.choices, default=PermissionRole.ALL
    )

    def search_indexable(self):
        return True

    def objecttype(self):
        return "resource"

    def get_resources(self, request):
        """Get the resources to show on the page."""
        basket = Basket(request.session)
        user_role = None
        user_details = request.session.get("UserDetails")
        key = quote(sign(self.permission_role))
        if user_details:
            user_role = user_details.get("ProductRegistrationVar1")

        def can_download(resource_item):
            if not resource_item.can_download:
                return False
            # If role is ALL, any user (including unauthenticated should be able to download)
            if self.permission_role == ResourcePage.PermissionRole.ALL:
                return True
            # TODO: user role is being converted to lowercase so that it can be compared to ResourcePage permission role
            # Ideally this would happen when the user is logged in
            if user_role and (
                user_role.lower() == self.permission_role
                or user_role.lower() == ResourcePage.PermissionRole.UBER
            ):
                return True
            return False

        def can_order(resource_item):
            if not user_role or not resource_item.can_order:
                return False
            if self.permission_role == ResourcePage.PermissionRole.ALL:
                return True
            if (
                user_role.lower() == self.permission_role
                or user_role.lower() == ResourcePage.PermissionRole.UBER
            ):
                return True
            return False

        return [
            {
                "items_in_basket_count": basket.get_item_count(resource.id),
                "image": resource.image,
                "title": resource.title,
                "can_download": resource.can_download,
                "permission_to_download": can_download(resource),
                "document": resource.document,
                "document_content": resource.document_content,
                "can_order": resource.can_order,
                "permission_to_order": can_order(resource),
                "maximum_order_quantity": resource.maximum_order_quantity,
                "sku": resource.sku,
                "image_alt_text": resource.image_alt_text,
                "key": key,
                "has_error": basket.get_item_has_error(resource.id),
                "item": basket.get_item(resource.id),
                "resource_page_id": self.id,
            }
            for resource in self.resource_items.select_related("image", "document")
        ]

    def get_az_item(self):
        resource_items = self.resource_items.select_related("image", "document")
        resource_item = resource_items[0] if (len(resource_items) > 0) else None
        campaign = self.get_parent()
        az_resource = {
            "objecttype": self.objecttype(),
            "object_url": f"{self.url}",
            "title": self.title,
            "campaign_title": campaign.title,
            "campaign_url": campaign.url,
            "description": self.description,
            "summary": self.summary,
            "taxonomy_json": self.taxonomy_json,
            "last_published_at": datetime.timestamp(self.last_published_at)
            if self.last_published_at
            else None,
            "code": self.slug,
            "permission_role": self.permission_role,
        }
        if resource_item:
            az_resource["image_url"] = (
                resource_item.image.get_rendition("width-400").url
                if resource_item.image
                else ""
            )
            az_resource["image_alt"] = (
                resource_item.image_alt_text if resource_item.image_alt_text else ""
            )
        return az_resource

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
        allowed = user_role and user_role != ""
        resources = self.get_resources(request)
        items = []
        for resource in resources:
            if resource.get("has_error"):
                item = resource.get("item")
                id = item.get("id")
                items.append((id, item))
        context.update(
            resources=resources,
            # TODO: this logged_in value could be potentially removed now
            logged_in=request.session.get("ParagonUser"),
            allowed=allowed,
            taxonomy_json=json_data,
            topics_present=get_taxonomies(json_data, "TOPIC"),
            targaud_present=get_taxonomies(json_data, "TARGAUD"),
            type_present=get_taxonomies(json_data, "TYPE"),
            items=items,
            has_errors=len(items) > 0,
        )
        return context

    search_fields = BasePage.search_fields + [
        index.SearchField("description"),
        index.SearchField("summary"),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("permission_role"),
                # FieldPanel("permission_email_domain"),
            ],
            heading="Permissions",
        ),
        FieldPanel("summary"),
        FieldPanel("description"),
        InlinePanel("resource_items", label="Resources"),
    ]

    settings_panels = BasePage.settings_panels + PageLifecycleMixin.panels

    taxonomy_panels = [
        TaxonomyPanel("taxonomy_json", taxonomy_terms_id=TAXONOMY_TERMS_ID)
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(taxonomy_panels, heading="Taxonomy"),
            ObjectList(BasePage.promote_panels, heading="Promote"),
            ObjectList(
                BasePage.settings_panels + PageLifecycleMixin.panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )


class ResourceItem(Orderable):
    resource_page = ParentalKey(ResourcePage, related_name="resource_items")
    title = models.CharField(max_length=50)
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose an image to display for the resource.",
    )
    can_download = models.BooleanField(
        default=False,
        help_text="Controls whether the resource can be downloaded from the "
        "site. A document must be choosen to enable this.",
    )
    document = models.ForeignKey(
        get_document_model_string(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose the relevant file from the \
        Wagtail document library.",
    )
    document_content = models.CharField(blank=True, null=True, max_length=50)
    image_alt_text = models.CharField(
        blank=True, null=True, max_length=50, help_text="Alt text for the image."
    )
    can_order = models.BooleanField(
        default=False,
        help_text="Controls whether physical copies of the resource can be "
        "ordered through the site. Only authenticated users can order resources.",
    )
    sku = models.CharField(
        blank=True,
        max_length=50,
        help_text="The stock control unit code for ordering physical copies "
        "of the resource. Required if 'Can Order' is checked.",
    )
    maximum_order_quantity = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="The maximum number of physical copies that can be ordered "
        "through the site. Required if 'Can Order' is checked.",
    )

    def clean(self):
        super().clean()
        errors = defaultdict(list)
        if self.can_download and not self.document:
            errors["document"].append("Please choose a document to download")
        if self.can_order and not self.sku:
            errors["sku"].append("Please enter a SKU")
        if self.can_order and not self.maximum_order_quantity:
            errors["maximum_order_quantity"].append(
                "Please enter a maximum order quantity"
            )
        if not (self.can_order or self.can_download):
            errors["can_download"].append(
                "Please enable one - 'can order' or 'can download' field"
            )
            errors["can_order"].append(
                "Please enable one - 'can order' or 'can download' field"
            )
        if errors:
            raise ValidationError(errors)

    panels = [
        FieldPanel("title"),
        ImageChooserPanel("image"),
        FieldPanel("image_alt_text"),
        FieldPanel("can_download"),
        DocumentChooserPanel("document"),
        FieldPanel("document_content"),
        FieldPanel("can_order"),
        FieldPanel("sku"),
        FieldPanel("maximum_order_quantity"),
    ]
