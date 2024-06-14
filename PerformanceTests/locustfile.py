import os
from locust import HttpUser, task
import urllib.parse
from re import match


class CRCBrowserUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BASE_URL = os.getenv("LOCUST_BASE_URL", "")
        self.CRC_EMAIL = os.getenv("LOCUST_CRC_EMAIL", "")
        self.CRC_PASSWORD = os.getenv("LOCUST_CRC_PASSWORD", "")
        self.basicHeaders = {
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.headersWithContentType = self.basicHeaders.copy()
        self.headersWithContentType[
            "Content-Type"
        ] = "application/x-www-form-urlencoded"

    def add_referer_header(self, dict, relativeUrl):
        dictWithReferer = dict.copy()
        dictWithReferer["Referer"] = self.BASE_URL + relativeUrl
        return dictWithReferer

    def send_get_request(self, relative_url, headers, referer=None):
        if referer:
            headers = self.add_referer_header(headers, referer)
        return self.client.get(relative_url, headers=headers, verify=False)

    def send_post_request(self, relative_url, body, headers, referer=None):
        if referer:
            headers = self.add_referer_header(headers, referer)
        return self.client.post(relative_url, data=body, headers=headers, verify=False)

    @task
    def login_download_order_logout(self):
        self.send_get_request("/", self.basicHeaders)

        login_response = self.send_get_request("/login/", self.basicHeaders)
        csrfCookie = match(
            r"csrftoken=([^;]+);", login_response.headers.get("set-cookie", "")
        )[1]

        self.send_post_request(
            "/login/",
            {
                "email": urllib.parse.quote(self.CRC_EMAIL),
                "password": urllib.parse.quote(self.CRC_PASSWORD),
                "previous_page": self.BASE_URL + "/",
                "csrfmiddlewaretoken": urllib.parse.quote(csrfCookie),
            },
            self.headersWithContentType,
            "/login/",
        )
        self.send_get_request("/campaigns/top-tips-for-teeth/", self.basicHeaders)
        self.send_get_request(
            "/campaigns/top-tips-for-teeth/a4-posters/", self.basicHeaders, "/login/"
        )

        self.send_get_request(
            "/crc-documents/278/29.09.2021A4_c4l_top_tips_teeth_poster_come_back_soon.pdf?a=gAAAAABmbDjMGqDEYY2dMGDWS_siX-qktsxK0_l6tCSX13_tFfIfA1S_UXJTa8YP4dAUTeYZD5KY29tTBMGqmGbFYFAaR111LxeF-zipxov8n5ioScTk6wCF44ZkBI0C510LQqNk2lroc-0gGko7MgkujS5eS25nKw%3D%3D",
            self.basicHeaders,
        ),

        self.send_post_request(
            "/baskets/add_item/",
            {
                "sku": urllib.parse.quote("C4L480"),
                "order_quantity": urllib.parse.quote("1"),
                "csrfmiddlewaretoken": urllib.parse.quote(csrfCookie),
            },
            self.headersWithContentType,
            "/campaigns/top-tips-for-teeth/a4-posters/",
        )

        self.send_get_request("/baskets/view_basket/", self.basicHeaders)

        self.send_get_request(
            "/orders/address/edit/", self.basicHeaders, "/orders/address/edit/"
        )

        self.send_post_request(
            "/orders/address/edit/",
            {
                "Address1": urllib.parse.quote("Somewhere"),
                "Address2": urllib.parse.quote("1"),
                "Address3": urllib.parse.quote("2"),
                "Address4": urllib.parse.quote("London"),
                "Address5": urllib.parse.quote("WC1 2AA"),
                "csrfmiddlewaretoken": urllib.parse.quote(csrfCookie),
            },
            self.headersWithContentType,
            "/orders/address/edit/",
        )

        self.send_post_request(
            "/orders/place/",
            {"csrfmiddlewaretoken": urllib.parse.quote(csrfCookie)},
            self.headersWithContentType,
            "/orders/address/edit/",
        )

        self.send_get_request("/logout", self.basicHeaders)
