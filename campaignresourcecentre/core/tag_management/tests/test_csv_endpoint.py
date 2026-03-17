import json

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from campaignresourcecentre.core.preparetestdata import PrepareTestData

User = get_user_model()


class SetTopicTagsFromCsvEndpointTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        td = PrepareTestData()
        cls.campaign_page = td.campaign_page
        cls.resource_page = td.resource_page
        cls.user = User.objects.get(username="wagtail")

    def setUp(self):
        self.url = reverse("set_topic_tags_from_csv")
        self.client.force_login(self.user)

    def _post_csv(self, csv_content):
        csv_file = SimpleUploadedFile(
            "tags.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )
        return self.client.post(self.url, {"file": csv_file})

    def test_sets_live_and_draft_tags_from_csv(self):
        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "ADULTS", "label": "Adults"},
            ]
        )
        self.campaign_page.save_revision(user=self.user).publish()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "DENTAL", "label": "Dental health"},
                {"code": "ADULTS", "label": "Adults"},
            ]
        )
        self.campaign_page.save_revision(user=self.user)

        csv_content = (
            "page_id,tags\n" f'{self.campaign_page.id},"Cancer, Coronavirus, Adults"\n'
        )
        response = self._post_csv(csv_content)

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["num_failed"], 0)
        self.assertEqual(payload["num_modified"], 1)

        self.campaign_page.refresh_from_db()
        live_tags = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual(
            {tag["code"] for tag in live_tags}, {"CANCER", "COVID", "ADULTS"}
        )

        latest_revision = self.campaign_page.latest_revision
        live_revision = self.campaign_page.live_revision
        self.assertNotEqual(latest_revision.id, live_revision.id)

        draft_tags = json.loads(latest_revision.as_object().taxonomy_json)
        self.assertEqual(
            {tag["code"] for tag in draft_tags}, {"CANCER", "COVID", "ADULTS"}
        )

    def test_returns_row_errors_and_continues_processing(self):
        csv_content = (
            "page_id,tags\n"
            f'{self.resource_page.id},"Coronavirus, Healthcare professionals"\n'
            "999999,Cancer\n"
            f"{self.campaign_page.id},Not a real tag\n"
        )

        response = self._post_csv(csv_content)

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["num_processed"], 3)
        self.assertEqual(payload["num_failed"], 2)
        self.assertEqual(payload["num_modified"] + payload["num_unchanged"], 1)

        row_results = {row["row"]: row for row in payload["results"]}
        self.assertIn(row_results[2]["status"], {"updated", "unchanged"})
        self.assertEqual(row_results[3]["status"], "error")
        self.assertIn("not found", row_results[3]["error"].lower())
        self.assertEqual(row_results[4]["status"], "error")
        self.assertIn("unknown tags", row_results[4]["error"].lower())

    def test_returns_bad_request_when_file_is_missing(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 400)
        self.assertIn("upload", response.json()["detail"].lower())

    def test_returns_bad_request_when_csv_is_completely_empty(self):
        response = self._post_csv("")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "CSV file is empty")

    def test_returns_bad_request_when_csv_has_only_blank_lines(self):
        response = self._post_csv("\n\n\n")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "CSV file is empty")

    def test_returns_bad_request_when_csv_has_only_a_header_row(self):
        response = self._post_csv("page_id,tags\n")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "CSV file is empty")

    def test_requires_admin_permission(self):
        basic_user = User.objects.create_user(username="basic-user", password="pass")
        self.client.force_login(basic_user)

        response = self._post_csv(f"{self.campaign_page.id},Cancer\n")

        self.assertEqual(response.status_code, 403)

    def test_endpoint_is_csrf_exempt(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)

        csv_file = SimpleUploadedFile(
            "tags.csv",
            f"{self.campaign_page.id},Cancer\n".encode("utf-8"),
            content_type="text/csv",
        )
        response = csrf_client.post(self.url, {"file": csv_file})

        self.assertEqual(response.status_code, 200)

    def test_replaces_only_topic_tags_and_preserves_non_topic_tags(self):
        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "CANCER", "label": "Cancer"},
                {"code": "ADULTS", "label": "Adults"},
            ]
        )
        self.campaign_page.save_revision(user=self.user).publish()

        self.campaign_page.taxonomy_json = json.dumps(
            [
                {"code": "DENTAL", "label": "Dental health"},
                {"code": "ADULTS", "label": "Adults"},
                {"code": "HEALTHPROFS", "label": "Healthcare professionals"},
            ]
        )
        self.campaign_page.save_revision(user=self.user)

        csv_content = "page_id,tags\n" f"{self.campaign_page.id},Coronavirus\n"
        response = self._post_csv(csv_content)

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["num_failed"], 0)
        self.assertEqual(payload["num_modified"], 1)

        self.campaign_page.refresh_from_db()
        live_tags = json.loads(self.campaign_page.taxonomy_json)
        self.assertEqual({tag["code"] for tag in live_tags}, {"COVID", "ADULTS"})

        latest_revision = self.campaign_page.latest_revision
        draft_tags = json.loads(latest_revision.as_object().taxonomy_json)
        self.assertEqual(
            {tag["code"] for tag in draft_tags},
            {"COVID", "ADULTS", "HEALTHPROFS"},
        )

        response_tags = {tag["code"] for tag in payload["results"][0]["tags"]}
        self.assertEqual(response_tags, {"COVID", "ADULTS"})
