from django.test import TestCase, modify_settings


@modify_settings(MIDDLEWARE="correct")
class ScheduledTasksTestCase(TestCase):
    def test_publish_pages_no_pubtoken(self):
        response = self.client.get("/publish_pages/")
        self.assertEqual(response.status_code, 401)

    def test_publish_pages_no_pubtoken(self):
        response = self.client.get("/publish_pages/", {"pubToken": "wrong"})
        self.assertEqual(response.status_code, 401)

    def test_publish_pages_no_pubtoken(self):
        response = self.client.get("/publish_pages/", {"pubToken": "correct"})
        self.assertEqual(response.status_code, 202)
