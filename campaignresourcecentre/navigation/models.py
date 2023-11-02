from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail import blocks
from wagtail.fields import StreamField


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False)
    title = blocks.CharBlock(
        help_text="Leave blank to use the page's own title. Add title if using the URL approach",
        required=False,
    )
    url = blocks.CharBlock(
        help_text="Only use if page does not exist in CMS", required=False
    )

    class Meta:
        template = ("molecules/navigation/blocks/menu_item.html",)


class LinkColumnWithHeader(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False, help_text="Leave blank if no header required."
    )
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        template = ("molecules/navigation/blocks/footer_column.html",)


@register_setting(icon="list-ul")
class NavigationSettings(BaseSiteSetting, ClusterableModel):
    primary_navigation = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Main site navigation",
        use_json_field=True,
    )
    secondary_navigation = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Alternative navigation",
        use_json_field=True,
    )
    footer_navigation = StreamField(
        [("column", LinkColumnWithHeader())],
        blank=True,
        help_text="Multiple columns of footer links with optional header.",
        use_json_field=True,
    )
    footer_links = StreamField(
        [("link", LinkBlock())],
        blank=True,
        help_text="Single list of elements at the base of the page.",
        use_json_field=True,
    )

    panels = [FieldPanel("primary_navigation"), FieldPanel("footer_links")]
