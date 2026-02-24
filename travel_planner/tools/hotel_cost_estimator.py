"""
Hotel cost estimator tool.
Estimates accommodation cost for a given city and number of nights.
"""
from typing import Any


def hotel_cost_estimator(city: str, days: int, budget: float) -> dict[str, Any]:
    """
    Estimate hotel/accommodation cost for a stay in a given city.

    Args:
        city: Destination city name (e.g. "Goa", "Mumbai").
        days: Number of nights of stay.
        budget: Total trip budget in currency (e.g. INR) for reference.

    Returns:
        Dict with estimated cost, tier suggestion, and breakdown.
    """
    city_lower = city.strip().lower()
    # Base nightly rates (INR) by tier - illustrative estimates per city
    tier_rates = {
        "budget": 1500,
        "mid": 3500,
        "luxury": 8000,
    }
    # Slight city multipliers for popular Indian destinations
    city_mult = 1.0
    if "goa" in city_lower:
        city_mult = 1.2
    elif "mumbai" in city_lower or "delhi" in city_lower:
        city_mult = 1.4
    elif "jaipur" in city_lower or "udaipur" in city_lower:
        city_mult = 1.1

    budget_per_night = budget / days if days > 0 else 0
    if budget_per_night >= 6000:
        tier = "luxury"
    elif budget_per_night >= 2500:
        tier = "mid"
    else:
        tier = "budget"

    rate = int(tier_rates[tier] * city_mult)
    total = rate * days

    return {
        "city": city,
        "days": days,
        "tier": tier,
        "estimated_per_night": rate,
        "total_estimated_cost": total,
        "currency": "INR",
        "breakdown": f"{tier} tier @ ~{rate} INR/night x {days} nights = {total} INR",
    }
