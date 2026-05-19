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


class ProblemBlock(blocks.StructBlock):
    """Custom Problem Section Block"""

    tag = blocks.CharBlock(label="Tag")
    heading = blocks.CharBlock(label="Überschrift")
    paragraph = blocks.CharBlock(label="Beschreibung")
    anchor = blocks.CharBlock(label="Anchor Link", required=False)


class ProblemCard(blocks.StructBlock):
    """ "Custom Problem Cards"""

    icon = ImageBlock(label="Icon")
    heading = blocks.CharBlock(label="Überschrift")
    paragraph = blocks.CharBlock(label="Beschreibung")


class HomePage(Page):
    """Homepage with dynamic content-blocks"""

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        print(context)
        return context

    hero = StreamField(
        [
            ("Hero", HeroBlock()),
        ],
        blank=True,
        null=True,
        max_num=1,
    )

    problem = StreamField(
        [
            ("Problem", ProblemBlock()),
        ],
        blank=True,
        null=True,
        max_num=1,
    )
    problem_card = StreamField(
        [
            ("ProblemCard", ProblemCard()),
        ],
        blank=True,
        null=True,
        max_num=3,
    )

    # solution=StreamField()
    # trust=StreamField()
    # process=StreamField()
    # contact=StreamField()

    content_panels = Page.content_panels + [
        FieldPanel("hero"),
        FieldPanel("problem"),
        FieldPanel("problem_card"),
    ]
