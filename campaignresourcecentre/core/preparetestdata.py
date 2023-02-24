# Class to populate the Wagtail database with some test pages

# Idempotent - makes no changes if it has already been run or if the
# named content is already present from manual editing

from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Model

from wagtail.core.models import Page, Site
from wagtail.documents import get_document_model
from wagtailreacttaxonomy.models import TaxonomyTerms

from campaignresourcecentre.campaigns.models import CampaignHubPage, CampaignPage
from campaignresourcecentre.resources.models import ResourcePage, ResourceItem

from campaignresourcecentre.core.assetdata import (
    TAXONOMY_TERMS_ID,
    TAXONOMY_TERMS_JSON,
    CAMPAIGN_IMAGE,
    RESOURCE_ITEM_IMAGE,
)


def make_wagtail_document(url, user, title):
    document_class = get_document_model()
    doc = document_class(uploaded_by_user=user)
    doc.save()
    return doc


def make_wagtail_image(url, title, name=None):
    from io import BytesIO

    from urllib import request
    import willow

    from django.core.files.images import ImageFile
    from wagtail.images import get_image_model

    image_class = get_image_model()

    content = request.urlopen(url).read()

    image_file = ImageFile(BytesIO(content), name=name if name is not None else url)

    im = willow.Image.open(BytesIO(content))
    width, height = im.get_size()

    image = image_class(title=title, file=image_file, width=width, height=height)
    image.save()

    return image


class PrepareTestData:
    def __init__(self):
        try:
            self._home = Page.objects.get(title="Campaign Resource Centre")
        except Page.DoesNotExist:
            self._home = Page.objects.get(title="Home")  # Should exist
            self._home.title = "Campaign Resource Centre"
        self._ensure_superuser("wagtail", "wagtail")
        self._ensure_taxonomy(TAXONOMY_TERMS_ID, TAXONOMY_TERMS_JSON)
        self._ensure_campaign_hub_page()
        self._ensure_campaign_page(
            "Change4Life",
            """
Change4Life aims to help families with children aged 5 to 11 to lead healthier lives by eating well and moving more.
            """,
            """
PHE's flagship social marketing programme, aimed at tackling obesity and encouraging families with children aged 5 to 11 to eat well and move more.
Change4Life aims to help families lead healthier lives by eating well and moving more. It is now a trusted and recognised brand, with 97% of mothers who have children aged 5 to 11 associating it with healthy eating.
            """,
            make_wagtail_image(CAMPAIGN_IMAGE, "Change4Life logo", "c4llogo"),
        )
        self._ensure_resource_page(
            "Top tips to keep your family happy and healthy leaflet",
            """Flyer for local authorities to send out with National Child Measurement Programme (NCMP) result letters to parents""",
            """This Change4Life top tips flyer (National Child Measurement Programme (NCMP) post-measurement information for parents) is for local authorities to send with the NCMP result letters to parents. The flyer provides simple tips to help families eat well and move more and highlights the additional ideas available on the Change4Life website.
For queries, please contact NCMP@phe.gov.uk for information on the NCMP or Partnerships@phe.gov.uk for information on ordering.""",
            "all",
        )
        self._ensure_resource_item(
            title="Healthy families top tips leaflet",
            image=make_wagtail_image(
                RESOURCE_ITEM_IMAGE,
                "C4L_Top_Tips_leaflet_Screen_thumbnail.jpg",
                "c4ltoptipsthumbnail",
            ),
            can_download=False,
            document=make_wagtail_document("url!", self.superuser, "Title"),
            can_order=True,
            sku="C4L301B",
            maximum_order_quantity=1000,
        )

    def _ensure_superuser(self, username, password):
        try:
            user_model = get_user_model()
            self.superuser = user_model.objects.create_superuser(
                username=username, email="superuser@example.com", password=password
            )
            self.superuser.save()
        except IntegrityError:
            self.superuser = user_model.objects.get(username=username)

    def _ensure_taxonomy(self, terms_id, terms_json):
        try:
            tt = TaxonomyTerms.objects.get(taxonomy_id=terms_id)
        except ObjectDoesNotExist:
            tt = TaxonomyTerms(taxonomy_id=terms_id, terms_json=terms_json)
            tt.save()

    def _ensure_campaign_hub_page(self):
        # Does the campaign hub page exist?
        try:
            self._chp = CampaignHubPage.objects.get()
        except CampaignHubPage.DoesNotExist:
            # Create a hub page
            chp_content_type = ContentType.objects.get_for_model(CampaignHubPage)
            self._chp = CampaignHubPage(
                title="Campaigns", content_type=chp_content_type, show_in_menus=True
            )
            sites = Site.objects.all()
            # Does a site exist
            if sites:
                # Assume first site is CRC
                site = sites[0]
                site.root_page = self._home
            else:
                # Create a CRC site
                site = Site.objects.create(
                    hostname="localhost", root_page=self._home, is_default_site=True
                )
            # Add our new hub page to the root
            site.save()
            self._home.specific.add_child(instance=self._chp)
            self._chp.save_revision().publish()
            self._chp.save()

    def _ensure_campaign_page(self, title, summary, description, img):
        try:
            self._cp = CampaignPage.objects.get(title=title)
        except CampaignPage.DoesNotExist:
            self._cp = CampaignPage(
                title=title,
                summary=summary,
                description=description,
                image=img,
                show_in_menus=True,
                last_published_at=datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            )
            self._chp.specific.add_child(instance=self._cp)
            self._cp.save_revision().publish()
            self._cp.save()

    def _ensure_resource_page(self, title, summary, description, permission_role="all"):
        try:
            self._rp = ResourcePage.objects.get(title=title)
        except ResourcePage.DoesNotExist:
            self._rp = ResourcePage(
                title=title,
                summary=summary,
                description=description,
                permission_role=permission_role,
                last_published_at=datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            )
            self._cp.specific.add_child(instance=self._rp)
            self._rp.save_revision().publish()
            self._rp.save()

    def _ensure_resource_item(
        self,
        title,
        image,
        can_download,
        can_order,
        sku,
        maximum_order_quantity,
        document,
    ):
        try:
            self._ri = ResourceItem.objects.get(title=title)
        except ResourceItem.DoesNotExist:
            self._ri = ResourceItem(
                resource_page=self._rp,
                title=title,
                image=image,
                can_download=can_download,
                can_order=can_order,
                sku=sku,
                maximum_order_quantity=maximum_order_quantity,
                document=document,
            )
            self._ri.save()

    @property
    def campaign_hub_page(self):
        return self._chp

    @property
    def campaign_page(self):
        return self._cp

    @property
    def resource_page(self):
        return self._rp

    @property
    def resource_item(self):
        return self._ri
