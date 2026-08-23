from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as pdfcanvas


DOC_TITLE = "Planning Poubelles et Ménage 2026"
DOC_SUBTITLE = "Règlement des poubelles et du ménage"

LEFT_MARGIN = 2 * cm
RIGHT_MARGIN = 2 * cm
TOP_MARGIN = 3.2 * cm      # room for the header drawn on every page
BOTTOM_MARGIN = 2.2 * cm   # room for the footer drawn on every page


class NumberedCanvas(pdfcanvas.Canvas):
    """
    Canvas that draws the header and the footer on every page.

    Pages are buffered so the footer can display "Page x / y" once the
    total number of pages is known.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self) -> None:
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self) -> None:
        total_pages = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header()
            self.draw_footer(total_pages)
            super().showPage()

        super().save()

    def draw_header(self) -> None:
        """Draw the title, the subtitle and the separator line on the page."""
        width, height = self._pagesize

        self.saveState()

        self.setFont('Helvetica-Bold', 16)
        self.setFillColor(colors.black)
        self.drawCentredString(width / 2.0, height - 1.8 * cm, DOC_TITLE)

        self.setFont('Helvetica-Oblique', 9)
        self.setFillColor(colors.grey)
        self.drawCentredString(width / 2.0, height - 2.4 * cm, DOC_SUBTITLE)

        self.setStrokeColor(colors.grey)
        self.setLineWidth(0.5)
        self.line(LEFT_MARGIN, height - 2.7 * cm, width - RIGHT_MARGIN, height - 2.7 * cm)

        self.restoreState()

    def draw_footer(self, total_pages: int) -> None:
        """Draw the separator line and the page number on the page."""
        width = self._pagesize[0]

        self.saveState()

        self.setStrokeColor(colors.grey)
        self.setLineWidth(0.5)
        self.line(LEFT_MARGIN, 1.7 * cm, width - RIGHT_MARGIN, 1.7 * cm)

        self.setFont('Helvetica', 8)
        self.setFillColor(colors.grey)
        self.drawCentredString(
            width / 2.0,
            1.2 * cm,
            f"Page {self._pageNumber} / {total_pages}"
        )

        self.restoreState()


def create_explanatory_pdf(output_file: str) -> None:
    """
    Create explanatory PDF for trash and cleaning schedule.

    Args:
        output_file: Output PDF file path
    """
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=DOC_TITLE,
        author="Les voisins"
    )
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    # Intro
    intro_text = """
    Chers voisins,<br/><br/>
    Voici une proposition de planning pour l'année 2026 ! 
    L'idée est simple : on se répartit les tâches 
    équitablement pour que tout le monde y trouve son compte. Vous trouverez ci-dessous 
    quelques explications sur le fonctionnement.
    """
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Section: Poubelles
    elements.append(Paragraph("Sortie des poubelles", heading_style))

    poubelles_text = """
    Deux collectes par semaine (parfois 3 les semaines avec jours fériés) :<br/>
    <b>• Poubelle bleue :</b> ordures ménagères.<br/>
    <b>• Poubelle jaune :</b> poubelle de tri.<br/><br/>
    Le numéro dans la colonne "Poubelles" indique l'étage responsable cette semaine-là. 
    On tourne sur un cycle de 4 semaines (3 → 2 → 1 → 0). Le jour indiqué est le jour où vous devez
    sortir la poubelle. Le ramassage a lieu le lendemain.<br/>
    <b>Rappel </b> : sortir la poubelle implique de l'amener au bout de la rue. 
    La personne en charge est également chargée de la ramener le lendemain 
    après le passage des services de la ville.
    """
    elements.append(Paragraph(poubelles_text, body_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Section: Ménage
    elements.append(Paragraph("Ménage de l'entrée", heading_style))

    menage_text = """
    Pour simplifier, le ménage est aligné sur le planning des poubelles : même semaine, 
    même étage responsable. Le ménage concerne uniquement les parties communes (entrée, 
    escaliers). Chacun balaie devant sa porte selon l'expression consacrée :)
    """
    elements.append(Paragraph(menage_text, body_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Section: Exception étage 0
    elements.append(Paragraph("Cas particulier : l'étage 0", heading_style))

    exception_text = """
    L'étage 0 ne participe pas au ménage car il habite à l'extérieur et n'utilise pas 
    les parties communes. Du coup, le ménage n'est pas fait une semaine sur quatre, 
    mais pas d'inquiétude, ça reste largement suffisant !
    """
    elements.append(Paragraph(exception_text, body_style))
    elements.append(Spacer(1, 0.4 * cm))

    # Conclusion
    conclusion_text = """
    Voilà, c'est tout simple ! Nous espérons que ça fonctionnera.<br/><br/>
    Bonne année 2026 et merci à tous pour votre participation ! 
    """
    elements.append(Paragraph(conclusion_text, body_style))

    # Build PDF
    doc.build(elements, canvasmaker=NumberedCanvas)


# Create explanatory PDF
create_explanatory_pdf('reglement_poubelles_menage_2026.pdf')

print("PDF généré : reglement_poubelles_menage_2026.pdf")
