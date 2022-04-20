from dataclasses import dataclass


@dataclass
class ContactUsData:
    email: str
    first_name: str
    last_name: str
    job_title: str
    organisation: str
    organisation_type: str
    campaign: str
    audience: str
    engagement: str
    promotion: str
    message: str
