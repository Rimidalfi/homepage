from django.db import models
from django.shortcuts import render
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import (
    EmailFormMixin,
    FormMixin,
    AbstractFormField,
)
from wagtail.contrib.forms.panels import FormSubmissionsPanel


class HeroBlock(blocks.StructBlock):
    """Custom Hero Block"""

    image = ImageBlock(label="Bild")
    cta = blocks.CharBlock(label="CTA")
    anchor = blocks.CharBlock(label="Anchor Link", required=False)
    anchor_name = blocks.CharBlock(label="Anchor Name", required=False)
    headline = blocks.RichTextBlock(label="Headline")
    sub_headline = blocks.RichTextBlock(label="Sub Headline", required=False)

    class Meta:
        icon = "image"
        template = "home/blocks/hero.html"


class ProblemCard(blocks.StructBlock):
    """Custom Problem Cards"""

    icon = ImageBlock(label="Icon")
    heading = blocks.CharBlock(label="Überschrift")
    paragraph = blocks.CharBlock(label="Beschreibung")

    class Meta:
        icon = "form"
        template = "home/blocks/problem_card.html"


class ProblemBlock(blocks.StructBlock):
    """Custom Problem Section Block"""

    tag = blocks.CharBlock(label="Tag")
    heading = blocks.CharBlock(label="Überschrift")
    paragraph = blocks.CharBlock(label="Beschreibung")
    anchor = blocks.CharBlock(label="Anchor Link", required=False)
    anchor_name = blocks.CharBlock(label="Anchor Name", required=False)
    # include ProblemCards
    cards = blocks.ListBlock(
        ProblemCard(),
        max_num=3,
        label="Problem Cards",
        required=False,
    )

    class Meta:
        icon = "thumbtack"
        template = "home/blocks/problem.html"


class FormSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, label="Überschrift")
    intro = blocks.RichTextBlock(required=False, label="Einleitung")
    anchor = blocks.CharBlock(required=False, label="Anchor Link")
    anchor_name = blocks.CharBlock(required=False, label="Anchor Name / HTML ID")
    submit_label = blocks.CharBlock(
        required=False, default="Absenden", label="Button Text"
    )

    class Meta:
        icon = "form"
        template = "home/blocks/form_section.html"


class HomePageFormField(AbstractFormField):
    page = ParentalKey(
        "home.HomePage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class HomePage(EmailFormMixin, FormMixin, Page):
    """Homepage with dynamic content-blocks"""

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("problem", ProblemBlock()),
            ("problem_card", ProblemCard()),
            ("form_section", FormSectionBlock()),
        ],
        blank=True,
        use_json_field=True,
        block_counts={
            "hero": {"min_num": 1, "max_num": 1},
            "problem": {"min_num": 1, "max_num": 1},
            "problem_card": {"min_num": 0, "max_num": 3},
            "form_section": {"min_num": 0, "max_num": 1},
        },
    )

    thank_you_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FormSubmissionsPanel(),
        InlinePanel("form_fields", label="Formularfelder"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address"),
                        FieldPanel("to_address"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="E-Mail",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["form"] = kwargs.get("form") or self.get_form(
            page=self,
            user=request.user,
        )
        return context

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = self.get_form(
                request.POST,
                request.FILES,
                page=self,
                user=request.user,
            )

            if form.is_valid():
                self.process_form_submission(form)

                if self.to_address:
                    self.send_mail(form)

                if request.headers.get("HX-Request") == "true":
                    return render(
                        request,
                        "home/partials/form_success.html",
                        {
                            "page": self,
                        },
                    )

                context = self.get_context(request, form=form, *args, **kwargs)
                return render(
                    request,
                    self.get_template(request, *args, **kwargs),
                    context,
                )

            if request.headers.get("HX-Request") == "true":
                return render(
                    request,
                    "home/partials/form_fields.html",
                    {
                        "page": self,
                        "form": form,
                        "submit_label": "Absenden",
                    },
                    status=422,
                )

            context = self.get_context(request, form=form, *args, **kwargs)
            return render(
                request,
                self.get_template(request, *args, **kwargs),
                context,
            )

        context = self.get_context(request, *args, **kwargs)
        return render(
            request,
            self.get_template(request, *args, **kwargs),
            context,
        )
