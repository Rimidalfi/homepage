from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageBlock


class HeroBlock(blocks.StructBlock):
    """Custom Hero Block"""

    image = ImageBlock(label="Bild")
    cta = blocks.CharBlock(label="CTA")
    anchor = blocks.CharBlock(label="Anchor Link", required=False)
    headline = blocks.RichTextBlock(label="Headline")
    sub_headline = blocks.RichTextBlock(label="Sub Headline", required=False)


class HomePage(Page):
    """Homepage with dynamic content-blocks"""

    hero = StreamField(
        [
            ("Hero", HeroBlock()),
        ],
        blank=True,
        null=True,
        max_num=1,
    )

    # problem=StreamField()
    # solution=StreamField()
    # trust=StreamField()
    # process=StreamField()
    # contact=StreamField()

    content_panels = Page.content_panels + [FieldPanel("hero")]
