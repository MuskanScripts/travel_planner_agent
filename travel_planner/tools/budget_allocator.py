"""
Budget allocator tool.
Allocates total budget across hotel, transport, and remaining for activities/food.
"""
from typing import Any


def budget_allocator(
    total_budget: float,
    hotel_cost: float,
    transport_cost: float,
) -> dict[str, Any]:
    """
    Allocate total budget: hotel, transport, and remainder for activities/food.

    Args:
        total_budget: Total trip budget (e.g. INR).
        hotel_cost: Estimated accommodation cost.
        transport_cost: Estimated transport cost.

    Returns:
        Dict with allocation breakdown and remaining budget.
    """
    fixed = hotel_cost + transport_cost
    remaining = max(0.0, total_budget - fixed)
    # Suggest split for activities vs food (50-50 of remaining)
    activities = remaining * 0.5
    food = remaining * 0.5

    return {
        "total_budget": total_budget,
        "hotel_allocation": hotel_cost,
        "transport_allocation": transport_cost,
        "fixed_total": fixed,
        "remaining_budget": remaining,
        "suggested_activities": round(activities, 2),
        "suggested_food": round(food, 2),
        "currency": "INR",
        "within_budget": fixed <= total_budget,
    }
