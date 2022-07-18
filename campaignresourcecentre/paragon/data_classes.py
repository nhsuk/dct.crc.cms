import datetime
from dataclasses import dataclass

from campaignresourcecentre.paragon_users.helpers.validate_password import (
    validate_password_data_classes,
)


@dataclass
class Registration:
    email: str
    password: str
    first_name: str
    last_name: str
    organisation: str
    job_title: str
    postcode: str
    created_at: datetime

    def valid(self):
        for key, value in self.__dict__.items():
            if not value:
                raise ValueError("{} is empty!".format(key))
        validate_password_data_classes(self.password)
        return True

    def params(self):
        self.valid()
        return {
            "EmailAddress": self.email,
            "Password": self.password,
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "ProductRegistrationVar2": "False",  # Is active
            "ProductRegistrationVar3": self.organisation,
            "ProductRegistrationVar4": self.job_title,
            "ProductRegistrationVar6": "true",  # Agreed to terms
            "ProductRegistrationVar7": "000000000000000000000000000000",
            "ProductRegistrationVar9": self.postcode,
            "ProductRegistrationVar10": self.created_at,
        }


@dataclass
class User:
    user_token: str
    email: str
    first_name: str
    last_name: str
    organisation: str
    job_title: str
    role: str
    active: str
    created_at: datetime
    verified_at: str
    subscriptions: str
    postcode: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def valid(self):
        if not self.user_token:
            raise ValueError("{} is empty!".format("user_token"))
        return True

    def params(self):
        self.valid()
        result = dict()
        result["UserToken"] = self.user_token
        if self.email:
            result["EmailAddress"] = self.email
        if self.first_name:
            result["FirstName"] = self.first_name
        if self.last_name:
            result["LastName"] = self.last_name
        if self.organisation:
            result["ProductRegistrationVar3"] = self.organisation
        if self.job_title:
            result["ProductRegistrationVar4"] = self.job_title
        if self.role:
            result["ProductRegistrationVar1"] = self.role
        if self.active:
            result["ProductRegistrationVar2"] = self.active
        if self.verified_at:
            result["ProductRegistrationVar8"] = self.verified_at
        if self.subscriptions:
            result["ProductRegistrationVar7"] = self.subscriptions
        if self.postcode:
            result["ProductRegistrationVar9"] = self.postcode
        if self.created_at:
            result["ProductRegistrationVar10"] = self.created_at

        return result


def datetime_from_str(datetime_str):
    if not datetime_str:
        return None
    suffix_idx = datetime_str.find(".")
    if suffix_idx > 0:
        cleaned_datetime_str = datetime_str[:suffix_idx]
    else:
        cleaned_datetime_str = datetime_str
    try:
        time_str = datetime.datetime.strptime(cleaned_datetime_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        time_str = datetime.datetime.strptime(
            cleaned_datetime_str, "%Y-%m-%d %H:%M:%S %z"
        )
    return time_str


def user_from_dict(user_dict):
    if "CreatedDate" in user_dict:
        created_at = datetime_from_str(user_dict["CreatedDate"])
    else:
        created_at = datetime_from_str(user_dict["ProductRegistrationVar10"])
    return User(
        user_token=user_dict["UserToken"],
        email=user_dict["EmailAddress"],
        first_name=user_dict["FirstName"],
        last_name=user_dict["LastName"],
        organisation=user_dict["ProductRegistrationVar3"],
        job_title=user_dict["ProductRegistrationVar4"],
        role=user_dict["ProductRegistrationVar1"],
        active=user_dict["ProductRegistrationVar2"],
        created_at=created_at,
        verified_at=user_dict["ProductRegistrationVar8"],
        subscriptions=user_dict["ProductRegistrationVar7"],
        postcode=user_dict["ProductRegistrationVar9"],
    )


@dataclass
class UpdatePassword:
    user_token: str
    password: str

    def valid(self):
        for key, value in self.__dict__.items():
            if not value:
                raise ValueError("{} is empty!".format(key))
        validate_password_data_classes(self.password)
        return True

    def params(self):
        self.valid()
        return {
            "UserToken": self.user_token,
            "Password": self.password,
        }


@dataclass
class Address:
    user_token: str
    address_lines: dict

    def valid(self):
        if not self.user_token:
            raise ValueError("{} is empty!".format("user_token"))
        return True

    def params(self):
        self.valid()
        return {
            "UserToken": self.user_token,
            "Address1": self.address_lines.get("Address1"),
            "Address2": self.address_lines.get("Address2"),
            "Address3": self.address_lines.get("Address3"),
            "Address4": self.address_lines.get("Address4"),
            "Address5": self.address_lines.get("Address5"),
        }


@dataclass
class CreateOrder:
    user_token: str
    order_number: str
    order_items: dict

    def valid(self):
        for key, value in self.__dict__.items():
            if not value:
                raise ValueError("{} is empty!".format(key))
        return True

    def checkout_items(self):
        checkout_items = []
        for item in self.order_items:
            checkout_item = {
                "ItemCode": item.get("item_code"),
                "Quantity": item.get("quantity"),
                "Url": item.get("url"),
                "Campaign": item.get("campaign"),
                "ImageUrl": item.get("image_url"),
                "Title": item.get("title"),
            }
            checkout_items.append(checkout_item)
        return checkout_items

    def params(self):
        self.valid()
        return {
            "UserToken": self.user_token,
            "CrcOrderNumber": self.order_number,
            "CheckoutItems": self.checkout_items(),
        }


# Class used when running performance tests outside of Paragon
@dataclass
class MockParagonResponse:
    status_code: int
    content: str = "{}"
