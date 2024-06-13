from locust import HttpUser, task


class CRCBrowserUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/", verify=False)
        self.client.get("/campaigns/", verify=False)
        self.client.get("/search/?q=", verify=False)
        self.client.get("/search/?q=NHS", verify=False)
