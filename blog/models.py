from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageBlock


class CustomImageBlock(blocks.StructBlock):
    """Added caption & heading text to ImageBlock()"""

    image = ImageBlock()
    heading = blocks.CharBlock(required=False)
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"


class BlogIndexPage(Page):
    """"""

    heading = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("intro"),
    ]

    # changing context with custom Query
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context


class BlogPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", CustomImageBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("date"),
        FieldPanel("body"),
        "gallery_images",
    ]


class BlogPageGalleryImage(Orderable):
    """"""

    page = ParentalKey(
        to=BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        to="wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(max_length=255, blank=True)
    panels = ["image", "caption"]
