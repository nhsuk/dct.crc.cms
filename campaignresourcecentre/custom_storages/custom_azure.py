import logging

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject

from urllib.parse import urlparse, urlunparse

from storages.backends.azure_storage import AzureStorage

logger = logging.getLogger(__name__)

class AzureMediaStorage (AzureStorage):
    account_name = getattr (settings, "AZURE_ACCOUNT_NAME", None)
    account_key = getattr (settings, "AZURE_ACCOUNT_KEY", None)
    azure_container = getattr (settings, "AZURE_CONTAINER", None)
    external_domain = getattr (settings, "AZURE_CUSTOM_DOMAIN", None)
    custom_domain = None

    def save(self, name, content, max_length=None):
        logger.info ("Saving %s in container %s of account %s" %
            (name, __class__.azure_container, __class__.account_name)
        )
        return super ().save (name, content, max_length)

    def __init__ (self, **settings):
        super ().__init__ (**settings)
        logger.info ("Using storage domain '%s' for media", self.custom_domain)

    def url(self, name, expire=None, parameters=None):
        initial_url = super().url (name, expire, parameters)
        components = list(urlparse(initial_url))
        components[1] = self.external_domain
        new_url = urlunparse(components)
        return new_url

class AzureSearchStorage (AzureStorage):
    account_name = getattr (settings, "AZURE_SEARCH_STORAGE_ACCOUNT_NAME", None)
    account_key = getattr (settings, "AZURE_SEARCH_ACCESS_KEY", None)
    azure_container = getattr (settings, "AZURE_SEARCH_CONTAINER", None)
    custom_domain = None

    def __init__ (self, **settings):
        super ().__init__ (**settings)
        logger.info ("Using storage domain '%s' for search", self.custom_domain)

# Based on default_storage in https://github.com/django/django/blob/main/django/core/files/storage.py
# Storage instance is only really instantiated after all settings are configured and in a request context

class SearchStorage (LazyObject):
    def _setup (self):
        self._wrapped = get_storage_class (
            getattr (settings, "SEARCH_STORAGE_CLASS", settings.DEFAULT_FILE_STORAGE)
        ) ()

search_storage = SearchStorage ()
