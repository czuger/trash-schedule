import csv
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
import json


def csv_to_weekly_dict(csv_file: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Read CSV file, subtract one day from each date, then group by week and color.

    Args:
        csv_file: Path to CSV file

    Returns:
        Dictionary organized by week with colors grouping shifted dates
    """
    weekly_calendar = defaultdict(lambda: defaultdict(list))

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            date_str = row['date']
            couleur = row['couleur']

            # Parse date and subtract one day
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            previous_day = date_obj - timedelta(days=1)
            previous_day_str = previous_day.strftime('%Y-%m-%d')

            # Get ISO week number of the previous day
            week_num = previous_day.isocalendar()[1]
            week_key = f"w{week_num:02d}"

            # Add shifted date to corresponding week and color
            weekly_calendar[week_key][couleur].append(previous_day_str)

    # Convert defaultdict to regular dict and sort
    result = {}
    for week in sorted(weekly_calendar.keys()):
        result[week] = dict(weekly_calendar[week])

    return result


# Read CSV and convert
calendrier_hebdo = csv_to_weekly_dict('calendrier_poubelles_2026.csv')

# Save to JSON
with open('calendrier_hebdo_2026.json', 'w', encoding='utf-8') as f:
    json.dump(calendrier_hebdo, f, indent=2, ensure_ascii=False)

# Display first weeks
for week in list(calendrier_hebdo.keys())[:5]:
    print(f"{week}: {calendrier_hebdo[week]}")

print(f"\nTotal semaines: {len(calendrier_hebdo)}")
