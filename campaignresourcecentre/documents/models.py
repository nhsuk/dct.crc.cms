from wagtail.documents.models import AbstractDocument
from wagtail.documents.models import Document as WagtailDocument

from django.db import models
from django.utils.translation import gettext_lazy as _

from campaignresourcecentre.custom_storages.custom_azure import doc_storage


class CustomDocument(AbstractDocument):
    admin_form_fields = WagtailDocument.admin_form_fields
    file = models.FileField(
        upload_to="documents", storage=doc_storage, verbose_name=_("file")
    )
