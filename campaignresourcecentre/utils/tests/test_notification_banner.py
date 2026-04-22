from django.test import TestCase
from wagtail.models import Site

from campaignresourcecentre.core.preparetestdata import PrepareTestData
from campaignresourcecentre.utils.models import NotificationBanner

BANNER_CONTENT = "Test notification content"


class NotificationBannerModelTests(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)

    def test_defaults(self):
        banner = NotificationBanner.objects.create(site=self.site)
        self.assertEqual(banner.heading, "Important")
        self.assertEqual(banner.heading_level, "h2")
        self.assertFalse(banner.show_on_campaigns_page)
        self.assertFalse(banner.show_on_campaign_page)
        self.assertFalse(banner.show_on_search_results)
        self.assertIn("digital-only service", banner.content)

    def test_str(self):
        banner = NotificationBanner.objects.create(site=self.site)
        self.assertIn(self.site.site_name or self.site.hostname, str(banner))


PAGE_FLAGS = {
    "campaigns_hub": "show_on_campaigns_page",
    "individual_campaign": "show_on_campaign_page",
    "search": "show_on_search_results",
}


class NotificationBannerDisplayTests(TestCase):
    def setUp(self):
        test_data = PrepareTestData()
        self.campaign_hub_page = test_data.campaign_hub_page
        self.campaign_page = test_data.campaign_page
        self.default_site = Site.objects.get(is_default_site=True)

    def _set_banner(self, page=None, show_banner=False, **kwargs):
        defaults = {
            "heading": "Important",
            "heading_level": "h2",
            "content": f"<p>{BANNER_CONTENT}</p>",
            "show_on_campaigns_page": False,
            "show_on_campaign_page": False,
            "show_on_search_results": False,
        }
        if page:
            defaults[PAGE_FLAGS[page]] = show_banner
        defaults.update(kwargs)
        NotificationBanner.objects.update_or_create(
            site=self.default_site, defaults=defaults
        )

    def test_campaigns_hub_shows_banner_when_enabled(self):
        self._set_banner("campaigns_hub", show_banner=True)
        response = self.client.get(self.campaign_hub_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BANNER_CONTENT)

    def test_campaigns_hub_hides_banner_when_disabled(self):
        self._set_banner("campaigns_hub", show_banner=False)
        response = self.client.get(self.campaign_hub_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, BANNER_CONTENT)

    def test_individual_campaign_shows_banner_when_enabled(self):
        self._set_banner("individual_campaign", show_banner=True)
        response = self.client.get(self.campaign_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BANNER_CONTENT)

    def test_individual_campaign_hides_banner_when_disabled(self):
        self._set_banner("individual_campaign", show_banner=False)
        response = self.client.get(self.campaign_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, BANNER_CONTENT)

    def test_search_shows_banner_when_enabled(self):
        self._set_banner("search", show_banner=True)
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BANNER_CONTENT)

    def test_search_hides_banner_when_disabled(self):
        self._set_banner("search", show_banner=False)
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, BANNER_CONTENT)

    def test_banner_renders_heading_and_content(self):
        self._set_banner(
            "campaigns_hub",
            show_banner=True,
            heading="Service update",
            content="<p>We have moved to digital only.</p>",
        )
        response = self.client.get(self.campaign_hub_page.url)
        self.assertContains(response, "Service update")
        self.assertContains(response, "We have moved to digital only.")

    def test_banner_renders_custom_heading_level(self):
        self._set_banner(
            "campaigns_hub",
            show_banner=True,
            heading="Notice",
            heading_level="h3",
        )
        response = self.client.get(self.campaign_hub_page.url)
        self.assertContains(response, "<h3")
        self.assertContains(response, "Notice")

    def test_banner_renders_h1_heading_level(self):
        self._set_banner("campaigns_hub", show_banner=True, heading_level="h1")
        response = self.client.get(self.campaign_hub_page.url)
        self.assertContains(response, "<h1")

    def test_page_renders_without_banner_setting(self):
        response = self.client.get(self.campaign_hub_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, BANNER_CONTENT)
