from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import HelpPanel

from .utils import get_next_review_duration


class NextReviewHelpPanel(HelpPanel):
    """Custom help panel to tell the user the next review date."""

    def render(self):
        self.content = self.get_content()
        return mark_safe(render_to_string(self.template, {"self": self}))

    def get_content(self):
        return mark_safe(
            render_to_string(
                "molecules/page_lifecycle/next_review_help_panel.html",
                {
                    "self": self,
                    "next_review": self.form.instance.next_review,
                    "next_review_duration": get_next_review_duration(),
                },
            )
        )
