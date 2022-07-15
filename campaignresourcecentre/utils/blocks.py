from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock

from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "molecules/streamfield/blocks/image_block.html"


class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    title = blocks.CharBlock(required=False)

    class Meta:
        icon = "doc-full-inverse"
        template = "molecules/streamfield/blocks/document_block.html"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(form_classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "molecules/streamfield/blocks/quote_block.html"


class LeftImageWithTextBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_alt_text = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(features=["bold", "italic"])

    class Meta:
        icon = "doc-full-inverse"
        template = "molecules/streamfield/blocks/left_image_with_text_block.html"


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock(features=["bold", "italic", "link"])
    show_numbering = blocks.BooleanBlock(
        required=False,
        help_text="Controls whether to show numbers next to the accordion items.",
    )
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock()),
                ("text", blocks.TextBlock()),
            ],
            icon="pilcrow",
        )
    )

    class Meta:
        icon = "collapse-up"
        template = "molecules/streamfield/blocks/accordion_block.html"


class TextWithImageStackBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=6,
        default=3,
        help_text="The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.",
    )
    text = blocks.RichTextBlock(features=["bold", "italic", "link"])
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        icon = "doc-full-inverse"
        template = "molecules/streamfield/blocks/text_with_image_stack_block.html"


# Main streamfield block to be inherited by Pages
class StoryBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    left_image_with_text = LeftImageWithTextBlock()
    accordion = AccordionBlock()
    text_with_image_stack = TextWithImageStackBlock()

    # These blocks have been hidden for now as they're not present on the
    # designs.
    # heading = blocks.CharBlock(
    #     form_classname="full title",
    #     icon="title",
    #     template="molecules/streamfield/blocks/heading_block.html",
    # )
    # image = ImageBlock()
    # quote = QuoteBlock()
    # embed = EmbedBlock()
    # call_to_action = SnippetChooserBlock(
    #     "utils.CallToActionSnippet",
    #     template="molecules/streamfield/blocks/call_to_action_block.html",
    # )
    # document = DocumentBlock()

    class Meta:
        template = "molecules/streamfield/stream_block.html"
