"""
Transport cost estimator tool.
Estimates flight and local transport cost between origin and destination.
"""
from typing import Any


def transport_cost_estimator(origin: str, destination: str) -> dict[str, Any]:
    """
    Estimate transport cost from origin to destination (flights + local).

    Args:
        origin: Origin city or location (e.g. "Mumbai", "Delhi").
        destination: Destination city (e.g. "Goa", "Kerala").

    Returns:
        Dict with flight estimate, local transport estimate, and total.
    """
    origin_lower = origin.strip().lower()
    dest_lower = destination.strip().lower()

    # Illustrative one-way flight estimates (INR) for common Indian routes
    route_estimates = {
        ("mumbai", "goa"): 4500,
        ("delhi", "goa"): 6500,
        ("bangalore", "goa"): 4000,
        ("mumbai", "kerala"): 5500,
        ("delhi", "kerala"): 7000,
        ("goa", "mumbai"): 4500,
        ("goa", "delhi"): 6500,
        ("kerala", "mumbai"): 5500,
    }
    key = (origin_lower, dest_lower)
    if key in route_estimates:
        flight_one_way = route_estimates[key]
    else:
        # Default by distance proxy
        flight_one_way = 5000

    flight_total = flight_one_way * 2  # round trip
    # Local transport (cabs, bikes, etc.) per day estimate
    local_per_day = 1500
    local_total = local_per_day * 4  # assume 4 days typical

    total = flight_total + local_total

    return {
        "origin": origin,
        "destination": destination,
        "flight_estimate_round_trip": flight_total,
        "local_transport_estimate": local_total,
        "total_transport_estimate": total,
        "currency": "INR",
        "breakdown": f"Flights: {flight_total} INR, Local: {local_total} INR",
    }
