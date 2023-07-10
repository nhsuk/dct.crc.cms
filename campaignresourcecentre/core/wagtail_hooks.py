from logging import getLogger

from django.conf import settings
from django.http import HttpResponseBadRequest
from wagtail import hooks

logger = getLogger(__name__)
