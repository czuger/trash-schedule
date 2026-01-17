from datetime import datetime, timedelta
from typing import List, Dict
import csv


def generate_collection_list(year: int = 2026) -> List[Dict[str, str]]:
    """
    Generate waste collection list.

    Args:
        year: The year for the calendar (default: 2026)

    Returns:
        List of dictionaries with date and bin color
    """
    collections = []

    # Start and end dates
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    current_date = start_date

    while current_date <= end_date:
        day_name = current_date.strftime('%A')
        date_str = current_date.strftime('%Y-%m-%d')

        # Monday: Yellow bin
        if day_name == 'Monday':
            collections.append({
                "date": date_str,
                "couleur": "jaune"
            })

        # Thursday: Blue bin
        elif day_name == 'Thursday':
            collections.append({
                "date": date_str,
                "couleur": "bleue"
            })

        current_date += timedelta(days=1)

    return collections


# Generate list
calendrier_2026 = generate_collection_list(2026)

# Save to CSV file
with open('calendrier_poubelles_2026.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'couleur'])
    writer.writeheader()
    writer.writerows(calendrier_2026)

print(f"Calendrier sauvegardé: {len(calendrier_2026)} collectes")
