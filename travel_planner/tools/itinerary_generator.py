"""
Itinerary generator tool.
Creates a day-by-day plan from destination, attractions list, and number of days.
"""
from typing import List, Union


def itinerary_generator(
    destination: str,
    attractions: Union[List[str], str],
    days: int,
) -> str:
    """
    Generate a day-by-day itinerary for a destination given a list of attractions.

    Args:
        destination: Name of the destination (e.g. "Goa").
        attractions: List of attraction names or descriptions.
        days: Number of days for the trip.

    Returns:
        A formatted string with day-by-day itinerary.
    """
    if isinstance(attractions, str):
        attractions = [a.strip() for a in attractions.split(",") if a.strip()]
    if not isinstance(attractions, list):
        attractions = list(attractions) if attractions else []
    attractions = [str(a).strip() for a in attractions if a]

    lines = [f"# {destination} – {days}-Day Itinerary", ""]
    per_day = max(1, (len(attractions) + days - 1) // days) if attractions else 2
    idx = 0
    for d in range(1, days + 1):
        lines.append(f"## Day {d}")
        day_attractions = attractions[idx : idx + per_day]
        idx += per_day
        if day_attractions:
            for a in day_attractions:
                lines.append(f"- {a}")
        else:
            lines.append("- Free time / local exploration")
        lines.append("")
    return "\n".join(lines).strip()
