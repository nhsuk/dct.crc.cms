from django.test import RequestFactory, TestCase, override_settings
from wagtail_factories import SiteFactory

from campaignresourcecentre.utils.context_processors import global_vars
from campaignresourcecentre.utils.factories import TrackingFactory


class TrackingTest(TestCase):
    def setUp(self):
        self.site = SiteFactory(
            site_name="campaignresourcecentre", is_default_site=True
        )
        self.tracking = TrackingFactory(site=self.site)

    @override_settings(SITE_BASE_URL="http://testserver")
    def test_context_processor(self):
        request = RequestFactory().get("/")
        request.site = self.tracking.site
        request.session = {}
        tracking = global_vars(request)
        self.assertEqual(
            tracking,
            {
                "GOOGLE_TAG_MANAGER_ID": "GTM-123456",
                "SEO_NOINDEX": False,
                "BASKET_ITEM_COUNT": 0,
                "CANONICAL_PATH": "http://testserver/",
            },
        )
