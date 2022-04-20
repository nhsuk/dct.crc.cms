# Django command to ensure there is minimal content in a new CRC Wagtail database for systematic testing

# Idempotent - should make no changes if it has already been run or if the 
# named content is already present from manual editing

# after containers started:

# dj migrate
# dj preparetestdata
# djrun

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

from .assetdata import *

def make_wagtail_document (url, user, title):
    Document = get_document_model ()
    doc = Document (uploaded_by_user=user)
    doc.save ()
    return doc

def make_wagtail_image (url, title, name=None):

    from io import BytesIO

    from urllib import request
    import willow

    from django.core.files.images import ImageFile
    from wagtail.images import get_image_model

    Image = get_image_model ()

    content = request.urlopen (url).read ()

    image_file = ImageFile(BytesIO(content),
        name=name if name is not None else url
    )

    im = willow.Image.open(BytesIO(content))
    width, height = im.get_size()

    image = Image(title=title, file=image_file, width=width, height=height)
    image.save()

    return image    

class Command(BaseCommand):
    help = 'Prepares pages for performance testing stories'
    requires_system_checks = False

    def _create_pages (self):
        # Find root of our page tree and the initial home page created by Wagtail
        root = Page.get_first_root_node()
        try:
            self._home = Page.objects.get (title="Campaign Resource Centre")
        except Page.DoesNotExist:
            self._home = Page.objects.get (title="Home")   # Should exist
            self._home.title = "Campaign Resource Centre"
            if self._verbosity > 0:
                self.stdout.write (f"Renamed home page")
        self._ensureSuperuser ("wagtail", "wagtail")
        self._ensureTaxonomy (TAXONOMY_TERMS_ID, TAXONOMY_TERMS_JSON)
        self._ensureCampaignHubPage ()
        self._ensureCampaignPage (
            "Change4Life",
            """
Change4Life aims to help families with children aged 5 to 11 to lead healthier lives by eating well and moving more.
            """,
            """
PHE's flagship social marketing programme, aimed at tackling obesity and encouraging families with children aged 5 to 11 to eat well and move more.
Change4Life aims to help families lead healthier lives by eating well and moving more. It is now a trusted and recognised brand, with 97% of mothers who have children aged 5 to 11 associating it with healthy eating.
            """,
            make_wagtail_image (CAMPAIGN_IMAGE, "Change4Life logo", "c4llogo")
        )
        self._ensureResourcePage (
            "Top tips to keep your family happy and healthy leaflet",
            """Flyer for local authorities to send out with National Child Measurement Programme (NCMP) result letters to parents""",
            """This Change4Life top tips flyer (National Child Measurement Programme (NCMP) post-measurement information for parents) is for local authorities to send with the NCMP result letters to parents. The flyer provides simple tips to help families eat well and move more and highlights the additional ideas available on the Change4Life website.
For queries, please contact NCMP@phe.gov.uk for information on the NCMP or Partnerships@phe.gov.uk for information on ordering.""",
            "all"
        )
        self._ensureResourceItem (
            title = "Healthy families top tips leaflet",
            image = make_wagtail_image (
                RESOURCE_ITEM_IMAGE,
                "C4L_Top_Tips_leaflet_Screen_thumbnail.jpg", "c4ltoptipsthumbnail"
            ),
            can_download = False,
            document = make_wagtail_document ("url!", self.superuser, "Title"),
            #document_content = models.CharField(blank=True, null=True, max_length=50)
            can_order = True,
            sku = "C4L301B",
            maximum_order_quantity = 1000
        )

    def _ensureSuperuser (self, username, password):
        try:
            userModel = get_user_model ()
            self.superuser = userModel.objects.create_superuser(
                username=username,
                email="superuser@example.com",
                password=password)
            self.superuser.save()
            if self._verbosity > 0:
                self.stdout.write (f"Created superuser '{username}'")
        except IntegrityError:
            if self._verbosity > 0:
                self.stdout.write (f"Superuser '{username}' is already present")
            self.superuser = userModel.objects.get (username=username)

    def _ensureTaxonomy (self, terms_id, terms_json):
        try:
            tt =TaxonomyTerms.objects.get (taxonomy_id=terms_id)
        except ObjectDoesNotExist:
            if self._verbosity > 0:
                self.stdout.write(f"Creating taxonomy terms id '{terms_id}'")
            tt = TaxonomyTerms (
                taxonomy_id = terms_id,
                terms_json = terms_json
            )
            tt.save ()

    def _ensureCampaignHubPage (self):
        # Does the campaign hub page exist?
        try:
            self._chp = CampaignHubPage.objects.get ()
        except CampaignHubPage.DoesNotExist:
            # Create a hub page
            chp_content_type = ContentType.objects.get_for_model(CampaignHubPage)
            if self._verbosity > 0:
                self.stdout.write("Creating campaign hub page")
            self._chp = CampaignHubPage (
                title = "Campaigns",
                content_type = chp_content_type,
                show_in_menus = True
            )
            sites = Site.objects.all ()
            # Does a site exist
            if sites:
                # Assume first site is CRC
                site = sites [0]
                site.root_page = self._home
            else:
                # Create a CRC site
                if self._verbosity > 0:
                    self.stdout.write("Creating CRC site")
                site = Site.objects.create(
                    hostname="localhost",
                    root_page=self._home,
                    is_default_site=True
                )
            # Add our new hub page to the root
            site.save ()
            self._home.specific.add_child (instance=self._chp)
            self._chp.save_revision().publish()
            self._chp.save ()

    def _ensureCampaignPage (self, title, summary, description, img):
        try:
            self._cp = CampaignPage.objects.get (title=title)
        except CampaignPage.DoesNotExist:
            if self._verbosity > 0:
                self.stdout.write ("Creating page for campaign '%s'" % title)
            self._cp = CampaignPage (
                title=title,
                summary=summary,
                description=description,
                image=img,
                show_in_menus = True,
                last_published_at=datetime.fromisoformat('2021-01-01T00:00:00+00:00')
            )
            self._chp.specific.add_child (instance=self._cp)
            self._cp.save_revision().publish()
            self._cp.save ()

    def _ensureResourcePage (self, title, summary, description, permission_role="all"):
        try:
            self._rp = ResourcePage.objects.get (title=title)
        except ResourcePage.DoesNotExist:
            if self._verbosity > 0:
                self.stdout.write ("Creating page for resource '%s'" % title)
            self._rp = ResourcePage (
                title=title,
                summary=summary,
                description=description,
                permission_role=permission_role,
                last_published_at=datetime.fromisoformat('2021-01-01T00:00:00+00:00')
            )
            self._cp.specific.add_child (instance=self._rp)
            self._rp.save_revision().publish()
            self._rp.save ()
    
    def _ensureResourceItem (self, title, image, can_download,
        can_order, sku, maximum_order_quantity, document):
        try:
            self._ri = ResourceItem.objects.get (title=title)
        except ResourceItem.DoesNotExist:
            if self._verbosity > 0:
                self.stdout.write ("Creating resource item '%s'" % title)
            self._ri = ResourceItem (
                resource_page= self._rp,
                title=title,
                image=image,
                can_download=can_download,
                can_order=can_order,
                sku=sku,
                maximum_order_quantity=maximum_order_quantity,
                document=document
            )
            self._ri.save ()

    def handle(self, *args, **kwargs):
        # The root Page and a default homepage are created by wagtail migrations
        # This command should be idempotent, i.e. it will leave pages intact if they exist already
        self._verbosity = kwargs["verbosity"]

        #try:
        self._create_pages()
        #except:
        #    pages = Page.objects.all ()
        #    for p in pages:
        #        print (p.specific_class, p)
        if self._verbosity > 0:
            msg = "Test pages successfully created."
            self.stdout.write(msg)