from wagtail.core.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtailnhsukfrontend.blocks import (
    ActionLinkBlock,
    BooleanBlock,
    CardBasicBlock,
    CardClickableBlock,
    CardFeatureBlock,
    CardImageBlock,
    FlattenValueContext,
    ImageBlock,
    IntegerBlock,
)

from campaignresourcecentre.utils.blocks import StoryBlock


class CampaignAccordianBlock(FlattenValueContext, StructBlock):
    title = CharBlock(required=True)
    summary = CharBlock(required=False)
    content = RichTextBlock(required=False)

    class Meta:
        template = "../templates/blocks/accordian.html"
        icon = "pick"


class CampaignAccordiansBlock(FlattenValueContext, StructBlock):
    accordian_sections = ListBlock(CampaignAccordianBlock)

    class Meta:
        template = "../templates/blocks/accordians.html"


class CrcActionLinkBlock(ActionLinkBlock):
    class Meta:
        template = "../templates/blocks/crc_action_link.html"


class TwoColContainerBlock(FlattenValueContext, StructBlock):
    class BodyStreamBlock(StreamBlock):
        richtext = RichTextBlock()
        image = ImageBlock()
        actionlink = CrcActionLinkBlock()

    left_column = BodyStreamBlock(required=True)
    right_column = BodyStreamBlock(required=True)
    toggle_column = BooleanBlock(
        default=False,
        required=False,
        help_text="This toggle will make a right hand side image appear above the text on mobile",  # noqa: E501
    )

    class Meta:
        template = "../templates/blocks/two_col_container.html"
        label = "Two-col Content"


class DetailsBlock(FlattenValueContext, StructBlock):
    title = CharBlock(required=False)
    text = RichTextBlock(required=False)

    class Meta:
        icon = "collapse-down"
        template = "../templates/blocks/details.html"


class CampaignDetailsBlock(StreamBlock):
    details = DetailsBlock()


class ContentLinkBLock(FlattenValueContext, StructBlock):
    text = RichTextBlock()
    button_text = CharBlock()
    button_url = URLBlock()

    class Meta:
        template = "../templates/blocks/content_link.html"
        icon = "doc-full"


class CrcCardImageBLock(CardImageBlock):
    alt_text = CharBlock(
        required=False,
        help_text="Leave blank if the image is purely decorative. Most images on CRC will not require alt text.",
    )

    class Meta:
        template = "../templates/blocks/card_image.html"


class CrcCardGroupBLock(FlattenValueContext, StructBlock):
    heading = CharBlock(required=False)
    heading_level = IntegerBlock(
        min_value=2,
        max_value=4,
        default=2,
        help_text="The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=4.",
    )
    column = ChoiceBlock(
        [("", "Full-width"), ("one-half", "One-half"), ("one-third", "One-third")],
        default="",
        required=False,
    )

    class BodyStreamBlock(StreamBlock):
        card_basic = CardBasicBlock()
        card_clickable = CardClickableBlock()
        card_image = CrcCardImageBLock()
        card_feature = CardFeatureBlock()

    body = BodyStreamBlock(required=True)

    class Meta:
        icon = "doc-full"
        template = "../templates/blocks/card_group.html"


class FeaturePanelBlock(FlattenValueContext, StructBlock):

    heading = CharBlock(required=True)
    heading_level = IntegerBlock(
        min_value=2,
        max_value=6,
        default=3,
        help_text="The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.",  # noqa: E501
    )
    heading_size = ChoiceBlock(
        [("", "Default"), ("small", "Small"), ("medium", "Medium"), ("large", "Large")],
        help_text="The heading size affects the visual size, this follows the front-end library's sizing.",  # noqa: E501
        required=False,
    )
    content_image = ImageChooserBlock(label="Image", required=True)
    alt_text = CharBlock(
        required=False,
        help_text="Leave blank if the image is purely decorative. Most images on CRC will not require alt text.",
    )
    body = RichTextBlock(Label="Content", required=False)
    url = URLBlock(
        label="URL",
        required=False,
        help_text="Optional; if there is a link, a button will appear at the bottom of the panel.",
    )
    internal_page = PageChooserBlock(
        label="Internal Page",
        required=False,
        help_text="Optional; if there is a link, a button will appear at the bottom of the panel.",
    )
    button_text = CharBlock(
        label="Button Text",
        required=False,
        help_text="The button appears if a url is entered or internal page is selected",
    )

    class Meta:
        label = "Feature Panel"
        icon = "doc-full"
        template = "../templates/blocks/feature_panel.html"


class TextStackImageBlock(FlattenValueContext, StructBlock):
    heading = CharBlock(required=False)
    heading_level = IntegerBlock(
        min_value=2,
        max_value=6,
        default=2,
        help_text="The heading level affects users with screen readers. Default=2, Min=2, Max=6.",  # noqa: E501
    )
    content = RichTextBlock(required=True)
    image = ListBlock(ImageBlock(required=True))

    class Meta:
        label = "Text Stack Image Block"
        template = "../templates/blocks/text_stack.html"
        icon = "doc-full-inverse"


class CommonBlocks(StreamBlock):

    Card_group = CrcCardGroupBLock()
    Accordian = CampaignAccordiansBlock()
    two_col_container = TwoColContainerBlock()
    details_block = DetailsBlock()
    feature_panel = FeaturePanelBlock()
    text_stack_img = TextStackImageBlock()
    content = RichTextBlock()


class Section(FlattenValueContext, StructBlock):

    section_title = CharBlock(required=False)
    heading_level = IntegerBlock(
        min_value=2,
        max_value=4,
        default=2,
        help_text="The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=4.",
    )
    section_text = CharBlock(required=False)

    layout = ChoiceBlock(
        choices=[
            ("full", "full width"),
            ("2col", "two columns"),
            ("2thirds", "two thirds"),
        ],
        required=True,
        default="full",
        help_text="Select a layout type."
        "for two columns:"
        "Components are added in the left column first, then it alternates",
    )

    background_colour = ChoiceBlock(
        choices=[("app-section--white", "white"), ("app-section--grey", "nhs grey")],
        default="app-section--white",
        help_text="set background colour for the section",
    )
    content_blocks = CommonBlocks()

    class Meta:
        template = "../templates/blocks/section.html"
        label = "Section"


class HomePageSection(Section):

    content_blocks = [
        ("content_link", ContentLinkBLock()),
        ("Common_Blocks", CommonBlocks()),
    ]


class GuidePageSection(Section):

    content_blocks = [("story", StoryBlock()), ("Common_Blocks", CommonBlocks())]


class AboutPageSection(StreamBlock):

    content_blocks = Section()


class HomePageBlocks(StreamBlock):

    content_link = ContentLinkBLock()
    Common_Blocks = CommonBlocks()
    section = HomePageSection()


class GuidePageBlocks(StreamBlock):

    story = StoryBlock()
    Common_Blocks = CommonBlocks()
    section = GuidePageSection()


class CampaignsPageBlocks(StreamBlock):
    common_blocks = CommonBlocks()
    section = GuidePageSection()
