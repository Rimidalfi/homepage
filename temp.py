# Importiert Djangos Model-Basis, damit wir eigene Datenbankfelder und Modelle definieren können.
from django.db import models

# Importiert render(), damit wir in serve() Templates direkt als HTTP-Response zurückgeben können.
# Warum? In Wagtail ist serve() praktisch dein "View-Einstiegspunkt" für eine Page.
from django.shortcuts import render

# Importiert ParentalKey aus modelcluster.
# Warum? Wagtail nutzt das für "Kind-Objekte", die direkt im Admin zusammen mit einer Seite bearbeitet werden können.
from modelcluster.fields import ParentalKey

# Importiert die Wagtail-Basisklasse Page.
# Warum? Jede echte Seite in Wagtail erbt am Ende von Page.
from wagtail.models import Page

# Importiert StreamField und RichTextField.
# Warum? StreamField für flexible Inhaltsblöcke, RichTextField für formatierbaren Text wie den Danke-Text.
from wagtail.fields import StreamField, RichTextField

# Importiert das Blocks-Modul.
# Warum? Damit bauen wir eigene StreamField-Blöcke wie form_section.
from wagtail import blocks

# Importiert Bildblöcke für andere Landingpage-Abschnitte wie Hero oder Problem Cards.
# Warum? Du hattest solche Blöcke schon in deinem Seitenaufbau.
from wagtail.images.blocks import ImageBlock

# Importiert die Panel-Klassen für den Wagtail-Admin.
# Warum? Damit definierst du, welche Felder im Editor sichtbar sind und wie sie gruppiert werden.
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)

# Importiert die Form-Mixins und die Basisklasse für einzelne Wagtail-Formfelder.
# Warum?
# - FormMixin / EmailFormMixin geben dir Formularlogik auf einer normalen Seite.
# - AbstractFormField ist die Basis für dynamisch pflegbare Formularfelder im Admin.
from wagtail.contrib.forms.models import (
    EmailFormMixin,
    FormMixin,
    AbstractFormField,
)

# Importiert das Admin-Panel für Formulareinsendungen.
# Warum? Damit du im Wagtail-Admin Einsendungen ansehen kannst.
from wagtail.contrib.forms.panels import FormSubmissionsPanel


# Definiert einen Hero-Block für dein StreamField.
# Warum? Das ist einer deiner bestehenden Inhaltsblöcke für die Landingpage.
class HeroBlock(blocks.StructBlock):

    # Bildfeld im Hero.
    # Warum? Damit Redakteure ein Hero-Bild im StreamField setzen können.
    image = ImageBlock(label="Bild")

    # Einfaches Textfeld für einen CTA-Text.
    # Warum? Für Button-Beschriftung oder kurzen CTA-Inhalt.
    cta = blocks.CharBlock(label="CTA")

    # Optionaler Anchor-Link-Wert.
    # Warum? Falls du im Frontend Scroll-Navigation oder IDs ansteuern willst.
    anchor = blocks.CharBlock(label="Anchor Link", required=False)

    # Optionaler Anchor-Name / HTML-ID.
    # Warum? Damit der Block im HTML gezielt adressierbar ist.
    anchor_name = blocks.CharBlock(label="Anchor Name", required=False)

    # RichText für die Hauptüberschrift.
    # Warum? Mehr Flexibilität als ein reines CharField, z. B. Zeilenumbrüche oder Hervorhebungen.
    headline = blocks.RichTextBlock(label="Headline")

    # Optionaler RichText für Unterüberschrift.
    # Warum? Hero-Bereich braucht oft ergänzenden Text unter dem Haupttitel.
    sub_headline = blocks.RichTextBlock(label="Sub Headline", required=False)

    # Meta-Konfiguration für den Block.
    class Meta:
        # Definiert das Icon im Wagtail-Admin.
        # Warum? Bessere Erkennbarkeit beim Bearbeiten im StreamField.
        icon = "image"

        # Legt das Template fest, mit dem dieser Block im Frontend gerendert wird.
        # Warum? Trennung von Python-Definition und HTML-Ausgabe.
        template = "home/blocks/hero.html"


# Definiert einen Problem-Block für deine Landingpage.
# Warum? Inhaltlich z. B. für "Welches Problem lösen wir?".
class ProblemBlock(blocks.StructBlock):

    # Kurzer Tag / Badge / Label.
    tag = blocks.CharBlock(label="Tag")

    # Überschrift des Problem-Abschnitts.
    heading = blocks.CharBlock(label="Überschrift")

    # Beschreibung des Problems.
    paragraph = blocks.CharBlock(label="Beschreibung")

    # Optionaler Anchor-Link.
    anchor = blocks.CharBlock(label="Anchor Link", required=False)

    # Optionaler Anchor-Name bzw. HTML-ID.
    anchor_name = blocks.CharBlock(label="Anchor Name", required=False)

    # Meta-Konfiguration des Blocks.
    class Meta:
        # Icon im Admin.
        icon = "placeholder"

        # Frontend-Template.
        template = "home/blocks/problem.html"


# Definiert einen einzelnen Problem-Card-Block.
# Warum? Für wiederholbare Karten mit Icon, Titel und Beschreibung.
class ProblemCardBlock(blocks.StructBlock):

    # Bild/Icon der Karte.
    icon = ImageBlock(label="Icon")

    # Titel der Karte.
    heading = blocks.CharBlock(label="Überschrift")

    # Beschreibungstext der Karte.
    paragraph = blocks.CharBlock(label="Beschreibung")

    # Meta-Konfiguration des Blocks.
    class Meta:
        # Admin-Icon.
        icon = "doc-empty-inverse"

        # Frontend-Template.
        template = "home/blocks/problem_card.html"


# Definiert den Block, der an einer beliebigen Stelle der Landingpage das Formular platziert.
# Warum? Genau damit kannst du im StreamField auswählen, wo der Kontaktbereich erscheint.
class FormSectionBlock(blocks.StructBlock):

    # Optionale Überschrift des Formularabschnitts.
    # Warum? Damit der Redakteur z. B. "Kontakt", "Anfrage", "Lass uns sprechen" setzen kann.
    heading = blocks.CharBlock(required=False, label="Überschrift")

    # Optionaler Einleitungstext über dem Formular.
    # Warum? Für kurze Erklärung, Vertrauenstext oder CTA-Kontext.
    intro = blocks.RichTextBlock(required=False, label="Einleitung")

    # Optionaler Anchor-Link-Wert.
    # Warum? Kann für Navigation/Verlinkung genutzt werden.
    anchor = blocks.CharBlock(required=False, label="Anchor Link")

    # Optionale HTML-ID bzw. Anchor-Name.
    # Warum? Damit die Section im DOM direkt anspringbar ist.
    anchor_name = blocks.CharBlock(required=False, label="Anchor Name / HTML ID")

    # Optionaler Button-Text.
    # Warum? Damit "Absenden" redaktionell überschrieben werden kann, z. B. mit "Nachricht senden".
    submit_label = blocks.CharBlock(
        required=False, default="Absenden", label="Button Text"
    )

    # Meta-Konfiguration des Blocks.
    class Meta:
        # Icon im StreamField-Chooser.
        icon = "form"

        # Template für das Frontend.
        # Warum? Hier wird später der HTMX-Form-Container ausgegeben.
        template = "home/blocks/form_section.html"


# Definiert das Modell für EIN einzelnes Formularfeld auf der HomePage.
# Warum? Wagtails Standard-Formbuilder braucht ein Modell, das von AbstractFormField erbt.
class HomePageFormField(AbstractFormField):

    # Verknüpft das einzelne Formularfeld mit genau einer HomePage.
    # Warum?
    # - ParentalKey erlaubt Inline-Bearbeitung im Seiteneditor.
    # - related_name="form_fields" ist wichtig, weil Wagtail darüber die Formularfelder einsammelt.
    page = ParentalKey(
        "home.HomePage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


# Definiert die eigentliche Landingpage.
# Warum?
# - Page macht daraus eine Wagtail-Seite.
# - FormMixin liefert Formular-Mechanik.
# - EmailFormMixin ergänzt E-Mail-Versand für Einsendungen.
class HomePage(EmailFormMixin, FormMixin, Page):

    # Zentrales StreamField für deine Landingpage-Inhalte.
    # Warum?
    # - Statt viele einzelne StreamFields zu haben, kannst du die Reihenfolge frei über "body" steuern.
    # - form_section ist hier nur ein Block unter mehreren.
    body = StreamField(
        [
            # Hero-Block für Hero-Bereich.
            ("hero", HeroBlock()),
            # Problem-Block für Problem-Sektion.
            ("problem", ProblemBlock()),
            # Problem-Card-Block für wiederholbare Karten.
            ("problem_card", ProblemCardBlock()),
            # Formular-Sektion als platzierbarer Block.
            ("form_section", FormSectionBlock()),
        ],
        blank=True,
        # Nutzt JSON-basierte Speicherung.
        # Warum? Das ist der moderne Standard für StreamField in neueren Wagtail-Versionen.
        use_json_field=True,
    )

    # RichText für den Erfolgstext nach erfolgreicher Einsendung.
    # Warum? Dieser Text wird später bei erfolgreichem Submit statt des Formulars angezeigt.
    thank_you_text = RichTextField(blank=True)

    # Definiert die Editieroberfläche im Wagtail-Admin.
    # Warum? Nur Felder/Abschnitte, die hier eingebunden sind, erscheinen im Seiteneditor.
    content_panels = Page.content_panels + [
        # Zeigt das StreamField body im Editor an.
        # Warum? Redakteure sollen die Landingpage-Blöcke frei anordnen können.
        FieldPanel("body"),
        # Zeigt Einsendungen im Admin an.
        # Warum? Damit du Form Submissions direkt in Wagtail sehen kannst.
        FormSubmissionsPanel(),
        # InlinePanel für die eigentlichen Formularfelder.
        # Warum? Hier pflegt der Redakteur Name, E-Mail, Nachricht usw.
        InlinePanel("form_fields", label="Formularfelder"),
        # Feld für den Danke-/Erfolgstext.
        # Warum? Dieser Text soll im Admin bearbeitbar sein.
        FieldPanel("thank_you_text"),
        # Gruppiert die E-Mail-Einstellungen in einen eigenen Bereich.
        # Warum? Bessere Übersicht im Admin.
        MultiFieldPanel(
            [
                # Packt From- und To-Adresse in eine Zeile.
                # Warum? Diese Felder gehören logisch zusammen.
                FieldRowPanel(
                    [
                        # Absenderadresse für Formular-Mails.
                        FieldPanel("from_address"),
                        # Empfängeradresse für Formular-Mails.
                        FieldPanel("to_address"),
                    ]
                ),
                # Betreff der Benachrichtigungs-Mail.
                FieldPanel("subject"),
            ],
            heading="E-Mail",
        ),
    ]

    # Baut zusätzlichen Template-Kontext für diese Seite.
    # Warum? Templates brauchen hier immer Zugriff auf ein Form-Objekt.
    def get_context(self, request, *args, **kwargs):

        # Holt zuerst den Standard-Kontext von Wagtail.
        # Warum? page, request-nahe Infos und andere Standardwerte sollen erhalten bleiben.
        context = super().get_context(request, *args, **kwargs)

        # Legt das Formular in den Kontext.
        # Warum?
        # - Wenn aus serve() schon ein invalides Formular übergeben wurde, nutzen wir genau dieses.
        # - Sonst bauen wir ein frisches, leeres Formular für die Erstansicht.
        context["form"] = kwargs.get("form") or self.get_form(
            page=self,
            user=request.user,
        )

        # Gibt den erweiterten Kontext an das Template zurück.
        # Warum? Damit home_page.html und das Formular-Partial mit "form" arbeiten können.
        return context

    # Überschreibt serve(), also den Request-Einstiegspunkt dieser Wagtail-Seite.
    # Warum? In Wagtail ist serve() der richtige Ort, um POST-Requests und Formularlogik zu behandeln.
    def serve(self, request, *args, **kwargs):

        # Prüft, ob das Formular abgesendet wurde.
        # Warum? POST bedeutet: Nutzer hat etwas geschickt, also müssen wir validieren.
        if request.method == "POST":

            # Baut das Formular aus POST-Daten und ggf. hochgeladenen Dateien.
            # Warum?
            # - request.POST enthält Textfelder.
            # - request.FILES wäre wichtig, falls später Upload-Felder dazukommen.
            # - page=self und user=request.user werden von Wagtails Formsystem erwartet.
            form = self.get_form(
                request.POST,
                request.FILES,
                page=self,
                user=request.user,
            )

            # Prüft, ob alle Formularfelder gültig sind.
            # Warum? Nur dann darf gespeichert und ggf. gemailt werden.
            if form.is_valid():

                # Speichert die Formulareinsendung.
                # Warum? Wagtail legt dadurch den Submission-Datensatz an.
                self.process_form_submission(form)

                # Prüft, ob eine Empfängeradresse gesetzt wurde.
                # Warum? Nur dann macht das Senden einer E-Mail Sinn.
                if self.to_address:

                    # Verschickt die Benachrichtigungs-E-Mail.
                    # Warum? EmailFormMixin bringt diese Funktionalität mit.
                    self.send_mail(form)

                # Prüft, ob der Request von HTMX kam.
                # Warum? Dann wollen wir nicht die ganze Seite neu rendern, sondern nur das Erfolgs-Fragment.
                if request.headers.get("HX-Request") == "true":

                    # Rendert nur den Success-Container zurück.
                    # Warum? HTMX ersetzt damit gezielt nur den Formularbereich im DOM.
                    return render(
                        request,
                        "home/partials/form_success.html",
                        {
                            # Übergibt die Seite ans Template.
                            # Warum? Das Success-Template braucht z. B. page.thank_you_text.
                            "page": self,
                        },
                    )

                # Baut bei normalem Nicht-HTMX-Request den Kontext neu auf.
                # Warum? Damit das Seitentemplate mit aktuellem Kontext gerendert wird.
                context = self.get_context(request, form=form, *args, **kwargs)

                # Rendert die normale Seite erneut.
                # Warum? Für klassische POST-Requests ohne HTMX.
                return render(
                    request,
                    self.get_template(request, *args, **kwargs),
                    context,
                )

            # Prüft erneut, ob es ein HTMX-Request mit ungültigem Formular war.
            # Warum? Bei HTMX wollen wir in diesem Fall nur das Formularfragment mit Fehlermeldungen zurückgeben.
            if request.headers.get("HX-Request") == "true":

                # Rendert nur das Formularfragment mit Validierungsfehlern.
                # Warum? So kann HTMX den vorhandenen Formularbereich direkt ersetzen.
                return render(
                    request,
                    "home/partials/form_fragment.html",
                    {
                        # Übergibt die Seite ans Partial.
                        "page": self,
                        # Übergibt das gebundene, ungültige Formular.
                        # Warum? Nur so erscheinen Fehlermeldungen und bereits eingegebene Werte wieder im Formular.
                        "form": form,
                        # Übergibt den Button-Text.
                        # Warum? Das Partial erwartet diesen Wert; hier gibt es einen Fallback.
                        "submit_label": "Absenden",
                    },
                    # Gibt 422 zurück.
                    # Warum? Semantisch korrekt für "Validierung fehlgeschlagen".
                    status=422,
                )

            # Baut für einen normalen Nicht-HTMX-POST mit Fehlern den Kontext.
            # Warum? Dann wird die ganze Seite mit dem invaliden Formular neu gerendert.
            context = self.get_context(request, form=form, *args, **kwargs)

            # Rendert die ganze Seite mit Fehlermeldungen.
            # Warum? Klassisches Server-Side-Formhandling ohne HTMX.
            return render(
                request,
                self.get_template(request, *args, **kwargs),
                context,
            )

        # Baut bei GET-Requests den Standard-Kontext.
        # Warum? Beim ersten Laden der Seite braucht das Template ein leeres Formular.
        context = self.get_context(request, *args, **kwargs)

        # Rendert die normale Seite bei einem GET-Request.
        # Warum? Das ist die Standardansicht der Landingpage.
        return render(
            request,
            self.get_template(request, *args, **kwargs),
            context,
        )
