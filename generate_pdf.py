import json
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def load_calendar(json_file: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Load weekly calendar from JSON file.

    Args:
        json_file: Path to JSON file

    Returns:
        Weekly calendar dictionary
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def cycle_floors(start: int, num_weeks: int) -> List[int]:
    """
    Generate floor cycle from 0 to 3, starting from a given floor.

    Args:
        start: Starting floor (0-3)
        num_weeks: Number of weeks to generate

    Returns:
        List of floor numbers (0-3)
    """
    floors = []
    current = start

    for _ in range(num_weeks):
        floors.append(current)
        current = (current - 1) % 4

    return floors


def get_cleaning_floor(floor: int) -> str:
    """
    Get cleaning assignment for a floor. Floor 0 doesn't clean.

    Args:
        floor: Floor number (0-3)

    Returns:
        Floor number as string or "-" if floor 0
    """
    if floor == 0:
        return "-"
    return str(floor)


def create_pdf(calendar: Dict[str, Dict[str, List[str]]], output_file: str) -> None:
    """
    Create PDF with trash collection and cleaning schedule table.

    Args:
        calendar: Weekly calendar dictionary
        output_file: Output PDF file path
    """
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Planning Poubelles et Ménage 2026", styles['Title'])
    elements.append(title)

    # Get sorted weeks
    weeks = sorted(calendar.keys())

    # Generate floor cycle starting at floor 3
    floors = cycle_floors(start=3, num_weeks=len(weeks))

    # Build table data
    data = [["Semaine", "Bleue", "Jaune", "Poubelles", "Ménage"]]

    for i, week in enumerate(weeks):
        bleue_dates = "\n".join(calendar[week].get("bleue", []))
        jaune_dates = "\n".join(calendar[week].get("jaune", []))
        etage = floors[i]
        menage = get_cleaning_floor(etage)

        # Remove 'w' prefix from week number
        week_num = week.replace("w", "")

        data.append([week_num, bleue_dates, jaune_dates, str(etage), menage])

    # Create table
    table = Table(data, colWidths=[50, 130, 130, 60, 60])

    # Style table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (1, 1), (1, -1), colors.lightblue),
        ('BACKGROUND', (2, 1), (2, -1), colors.lightyellow),
        ('BACKGROUND', (4, 1), (4, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)
    elements.append(table)

    # Build PDF
    doc.build(elements)


# Load calendar and create PDF
calendar = load_calendar('calendrier_hebdo_2026.json')
create_pdf(calendar, 'planning_poubelles_2026.pdf')

print("PDF généré : planning_poubelles_2026.pdf")
