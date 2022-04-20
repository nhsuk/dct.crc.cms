from wagtail.admin.forms import WagtailAdminPageForm

from .utils import calculate_next_review_date


class PageLifecycleForm(WagtailAdminPageForm):
    """Custom form for managing page lifecyle."""

    def clean(self):
        cleaned_data = super().clean()

        # update the `next_review` date if the `last_reviewed` date has been
        # changed.
        if cleaned_data["last_reviewed"] != self.instance.last_reviewed:
            self.instance.next_review = calculate_next_review_date(
                cleaned_data["last_reviewed"]
            )
        return cleaned_data
