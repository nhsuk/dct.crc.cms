from datetime import datetime
import json
import logging
import requests
import uuid

from django.conf import settings
from .data_classes import (
    Registration,
    User,
    UpdatePassword,
    Address,
    CreateOrder,
    MockParagonResponse,  # For performance testing
)
from .exceptions import ParagonClientError, ParagonClientTimeout

logger = logging.getLogger(__name__)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = ":ECDH+AES256:DH+AES256:!DH"


class Client:
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.data = {"ProductToken": settings.PARAGON_API_KEY}
        # For performance testing - determine whether we are operating in a test environment
        # self.may_mock = settings.PARAGON_MOCK is not None and\
        #    settings.PARAGON_MOCK.lower ().startswith ("t")
        self.may_mock = settings.PARAGON_MOCK
        self.log_uuid = str(uuid.uuid4())

    # Original/production call to Paragon
    def _call(self):
        start_time = datetime.now()

        logger.info(
            json.dumps(
                {
                    "message": "Starting Paragon client call %s" % self.call_method,
                    "correlation_id": self.log_uuid,
                }
            )
        )

        try:
            self.response = requests.post(
                "{0}{1}".format(settings.PARAGON_API_ENDPOINT, self.call_method),
                headers=self.headers,
                json=self.data,
                timeout=settings.PARAGON_LOGIN_TIMEOUT_SECONDS,
            )
        except requests.Timeout:
            logger.error(
                json.dumps(
                    {
                        "message": "Paragon client timeout exceeded",
                        "type": "ParagonClientTimeout",
                        "endpoint": self.call_method,
                        "elapsed": (datetime.now() - start_time).total_seconds(),
                        "timeoutLimit": settings.PARAGON_LOGIN_TIMEOUT_SECONDS,
                        "correlation_id": self.log_uuid,
                    }
                )
            )
            raise ParagonClientTimeout

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(
            json.dumps(
                {
                    "message": "Paragon client %s call took %0.3fs"
                    % (self.call_method, elapsed),
                    "correlation_id": self.log_uuid,
                }
            )
        )

    # Revised call - delegates to either mock or real API
    def call(self):
        if self.may_mock:  # Is this a mocking client?
            # Decide whether to mock this specific call, or not
            if self.call_method == "/Login":
                self.response = MockParagonResponse(
                    content=json.dumps({"ParagonUser": "A token token"}),
                    status_code=200,
                )
            elif self.call_method == "/RetrieveProfile":
                self.response = MockParagonResponse(
                    status_code=200,
                    content=json.dumps(
                        {
                            "UserToken": "token token",
                            "ProductToken": "the product",
                            "Title": "mr",
                            "FirstName": "r",
                            "LastName": "c",
                            "EmailAddress": "testemail@email.com",
                            "ContactVar1": "1",
                            "ContactVar2": "1",
                            "ContactVar3": "1",
                            "ContactVar4": "1",
                            "ContactVar5": "1",
                            "ProductRegistrationVar1": "standard",  # or "uber"
                            "ProductRegistrationVar2": "True",
                            "ProductRegistrationVar3": "A mockery",
                            "ProductRegistrationVar4": "other",
                            "ProductRegistrationVar5": "1",
                            "ProductRegistrationVar6": "true",
                            "ProductRegistrationVar7": "1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                            "ProductRegistrationVar8": "2021-09-30T16:45",
                            "ProductRegistrationVar9": "WC1 2AA",
                            "ProductRegistrationVar10": "2021-09-30T16:40",
                        }
                    ),
                )
            else:
                self.response = MockParagonResponse(status_code=200)
        else:
            self._call()

    def raise_exception(self):
        logger.error(
            json.dumps(
                {
                    "error": "Paragon client request unsuccessful",
                    "endpoint": self.call_method,
                    "response": json.loads(self.response.content),
                    "status": self.response.status_code,
                    "elapsed": self.response.elapsed.total_seconds(),
                }
            )
        )
        raise ParagonClientError(json.loads(self.response.content))

    def create_account(
        self,
        email,
        password,
        first_name,
        last_name,
        organisation,
        job_title,
        area_work,
        postcode,
        postcode_region,
        created_at,
    ):
        self.call_method = "/Signup"
        registration = Registration(
            email,
            password,
            first_name,
            last_name,
            organisation,
            job_title,
            area_work,
            postcode,
            postcode_region,
            created_at,
        )
        self.data.update(registration.params())

        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def login(self, email, password):
        self.call_method = "/Login"
        self.data.update({"EmailAddress": email, "Password": password})
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def search_users(self, string, limit=20, offset=0):
        self.call_method = "/Search"
        self.data.update(
            {
                "EmailAddress": string,
                "FirstName": string,
                "LastName": string,
                "SortColumn": 0,  # Sort by created at
                "Top": limit,
                "Offset": offset,
            }
        )
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def get_user_profile(self, user_token):
        self.call_method = "/RetrieveProfile"
        self.data.update({"UserToken": user_token})
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def update_user_profile(
        self,
        user_token,
        email=None,
        first_name=None,
        last_name=None,
        organisation=None,
        job_title=None,
        role=None,
        active=None,
        verified_at=None,
        subscriptions=None,
        postcode=None,
        postcode_region=None,
        area_work=None,
    ):
        self.call_method = "/UpdateProfile"
        user_profile = User(
            user_token,
            email,
            first_name,
            last_name,
            organisation,
            job_title,
            area_work,
            role,
            active,
            "",
            verified_at,
            subscriptions,
            postcode,
            postcode_region,
        )
        self.data.update(user_profile.params())
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def update_password(self, user_token, password):
        self.call_method = "/UpdatePassword"
        update_password = UpdatePassword(user_token, password)
        self.data.update(update_password.params())
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def get_user_address(self, user_token):
        self.call_method = "/RetrieveDeliveryAddress"
        self.data.update({"UserToken": user_token})
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def set_user_address(self, user_token, address_lines):
        self.call_method = "/SetDeliveryAddress"
        address = Address(user_token, address_lines)
        self.data.update(address.params())
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def order_history(self, user_token, start_date, end_date, page_number, page_size):
        self.call_method = "/GetOrderHistory"
        self.data.update(
            {
                "UserToken": user_token,
                "StartDate": start_date,
                "EndDate": end_date,
                "PageNo": page_number,
                "PageSize": page_size,
            }
        )
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()

    def create_order(self, user_token, order_number, order_items):
        self.call_method = "/CreateCheckout"
        order = CreateOrder(user_token, order_number, order_items)
        self.data.update(order.params())
        self.call()
        if self.response.status_code == 200:
            return {
                "status": "ok",
                "code": self.response.status_code,
                "content": json.loads(self.response.content),
            }
        else:
            self.raise_exception()
