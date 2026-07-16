from django import template
from wagtail.models import Site
from wagtail.blocks.stream_block import StreamValue
from base.models import FooterText
from home.models import HomePage

register = template.Library()


# custom footer_text tag is registered which includes html and process logic
@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }


@register.inclusion_tag("base/includes/nav_links.html", takes_context=True)
def get_nav_links(context):
    nav_links = context.get("nav_links", "")

    # check if context is already available
    if not nav_links:

        # get anchor data for context
        try:
            instance = HomePage.objects.first()
            anchors = []
            # get site_root for url formation
            request = context.get("request")
            rootpage = (
                Site.find_for_request(context["request"]).root_page if request else None
            )

            # getting anchor data from streamValue fields
            for field in instance._meta.fields:

                value = getattr(instance, field.name, None)

                if type(value) == StreamValue:

                    for v in value:
                        # check for fields with anchor in it
                        if "anchor" in v.value:

                            block = v.value
                            anchors.append(
                                {
                                    "anchor_link": block["anchor"],
                                    "anchor_name": block["anchor_name"],
                                }
                            )
                    return {"nav_links": anchors, "site_root": rootpage}

        except Exception as e:
            print("EXEPTION: ", e)
            return {"nav_links": ""}


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page
