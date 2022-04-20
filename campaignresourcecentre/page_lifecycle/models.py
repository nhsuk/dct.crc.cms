from datetime import date

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Page

from .edit_handlers import NextReviewHelpPanel
from .forms import PageLifecycleForm
from .utils import calculate_next_review_date


class PageLifecycleMixin(models.Model):
    """Add to pages that need to notify users when they're due to be reviewed."""

    last_reviewed = models.DateField(default=date.today)
    next_review = models.DateField(default=calculate_next_review_date)

    class Meta:
        abstract = True

    panels = [
        MultiFieldPanel(
            [
                NextReviewHelpPanel(),
                FieldPanel("last_reviewed"),
                FieldPanel("owner"),
            ],
            heading="Page Lifecycle",
        )
    ]


class PageLifecyclePage(PageLifecycleMixin, Page):
    """Page type to test the PageLifecycleMixin, not used in the CMS."""

    is_creatable = False
    base_form_class = PageLifecycleForm
    content_panels = Page.content_panels + PageLifecycleMixin.panels

    @classmethod
    def search_indexable (cls):
        return False

@register_setting
class PageLifecycleSettings(BaseSetting):
    """Page lifecycle settings surfaced in the Wagtail admin."""

    notification_email = models.EmailField(
        max_length=255,
        help_text="Enter the email address that will receive page review "
        "notifications.",
    )
