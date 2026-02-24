"""
Rule-based intent detection for the Smart Travel Planner root agent.
Detects: greeting, incomplete request, or complete request (ready for orchestration).
"""
import re
from typing import Any


# Greeting phrases (case-insensitive match after strip)
GREETING_PHRASES = {
    "hi",
    "hello",
    "hey",
    "hey there",
    "good morning",
    "good afternoon",
    "good evening",
    "good night",
    "greetings",
    "howdy",
    "hi there",
    "hello there",
}


def get_travel_intent(user_message: str) -> dict[str, Any]:
    """
    Rule-based intent detection. Use this before triggering the travel planning pipeline.

    Args:
        user_message: The user's latest message (e.g. from the conversation).

    Returns:
        Dict with:
        - intent: "greeting" | "incomplete" | "complete"
        - greeting_response: (if greeting) suggested reply
        - missing_fields: (if incomplete) list of missing required fields
        - clarifying_suggestion: (if incomplete) suggested question to ask
        - has_destination, has_days_or_dates, has_budget: booleans for validation
    """
    if not user_message or not isinstance(user_message, str):
        return {
            "intent": "incomplete",
            "missing_fields": ["destination", "number of days or dates", "budget"],
            "clarifying_suggestion": "Please tell me where you want to go, for how many days (or which dates), and your budget.",
            "has_destination": False,
            "has_days_or_dates": False,
            "has_budget": False,
        }

    text = user_message.strip().lower()
    if len(text) > 200:
        text_for_greeting = text[:200]
    else:
        text_for_greeting = text

    # 1) Greeting detection: short message that is only a greeting
    text_normalized = re.sub(r"[\!\?\.\,]+$", "", text).strip()
    if len(text.split()) <= 4:
        if text in GREETING_PHRASES or text_for_greeting in GREETING_PHRASES:
            return {
                "intent": "greeting",
                "greeting_response": (
                    "Hello! I'm your Smart Travel Planner ✈️\n"
                    "Please tell me your destination, travel dates, budget, and preferences."
                ),
                "missing_fields": [],
                "clarifying_suggestion": "",
                "has_destination": False,
                "has_days_or_dates": False,
                "has_budget": False,
            }
        if text_normalized in GREETING_PHRASES:
            return {
                "intent": "greeting",
                "greeting_response": (
                    "Hello! I'm your Smart Travel Planner ✈️\n"
                    "Please tell me your destination, travel dates, budget, and preferences."
                ),
                "missing_fields": [],
                "clarifying_suggestion": "",
                "has_destination": False,
                "has_days_or_dates": False,
                "has_budget": False,
            }
        # Single word that looks like greeting
        if text_normalized in ("hi", "hey", "hello"):
            return {
                "intent": "greeting",
                "greeting_response": (
                    "Hello! I'm your Smart Travel Planner ✈️\n"
                    "Please tell me your destination, travel dates, budget, and preferences."
                ),
                "missing_fields": [],
                "clarifying_suggestion": "",
                "has_destination": False,
                "has_days_or_dates": False,
                "has_budget": False,
            }

    # 2) Extract required fields (simple rule-based)
    has_destination = _has_destination(text, user_message)
    has_days_or_dates = _has_days_or_dates(text, user_message)
    has_budget = _has_budget(text, user_message)

    # 3) Complete: all required fields present
    if has_destination and has_days_or_dates and has_budget:
        return {
            "intent": "complete",
            "missing_fields": [],
            "clarifying_suggestion": "",
            "has_destination": True,
            "has_days_or_dates": True,
            "has_budget": True,
        }

    # 4) Incomplete: build missing list and suggestion
    missing = []
    if not has_destination:
        missing.append("destination (e.g. city or region)")
    if not has_days_or_dates:
        missing.append("number of days or travel dates")
    if not has_budget:
        missing.append("budget (e.g. in INR or your currency)")

    suggestion = (
        "I'd be happy to plan your trip. To get started, I need a few details: "
        + "; ".join(missing)
        + ". Please share these so I can create your itinerary."
    )

    return {
        "intent": "incomplete",
        "missing_fields": missing,
        "clarifying_suggestion": suggestion,
        "has_destination": has_destination,
        "has_days_or_dates": has_days_or_dates,
        "has_budget": has_budget,
    }


def _has_destination(text_lower: str, original: str) -> bool:
    """Heuristic: trip to X, in X, X trip, visit X, destination X, goa, mumbai, etc."""
    # "trip to Goa", "go to Kerala", "visit Mumbai", "in Goa", "Goa trip", "destination: Delhi"
    if re.search(r"\b(trip to|go to|visit|in|to)\s+[a-z\u0900-\u097f]+", text_lower):
        return True
    if re.search(r"\b(destination|place|city)\s*[:\s]*[a-z\u0900-\u097f]+", text_lower):
        return True
    # Standalone place names (common Indian destinations)
    places = (
        "goa", "mumbai", "delhi", "kerala", "rajasthan", "jaipur", "udaipur",
        "bangalore", "chennai", "hyderabad", "kolkata", "manali", "rishikesh",
        "andaman", "darjeeling", "shimla", "agra", "varanasi", "ladakh",
    )
    for p in places:
        if p in text_lower:
            return True
    # "X trip" or "X travel" where X is a place name (at least 3 chars, not stopwords)
    if re.search(r"\b([a-z\u0900-\u097f]{3,})\s+(trip|travel)\b", text_lower):
        return True
    return False


def _has_days_or_dates(text_lower: str, original: str) -> bool:
    """Heuristic: N day(s), N-day, for N days, dates, next week, etc."""
    # "4 days", "4-day", "for 5 days", "3 nights"
    if re.search(r"\b(\d+)\s*[-]?\s*(day|night)s?\b", text_lower):
        return True
    if re.search(r"\b(for|of)\s+\d+\s+(day|night)", text_lower):
        return True
    # "dec 25", "next week", "january", "dates"
    if re.search(r"\b(next week|next month|dates?|travel dates)\b", text_lower):
        return True
    if re.search(r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b", text_lower):
        return True
    if re.search(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b", original):
        return True
    return False


def _has_budget(text_lower: str, original: str) -> bool:
    """Heuristic: ₹X, INR X, Rs. X, X budget, X rupees."""
    # ₹50000, Rs. 50000, INR 50000, 50k, 50,000
    if re.search(r"[₹rs\.\s]*(inr)?\s*[\d,]+(\s*(k|thousand|lakh|lac|rupees?|inr))?", text_lower):
        return True
    if re.search(r"\bbudget\s*[:\s]*[\d,]+", text_lower):
        return True
    if re.search(r"[\d,]+\s*(k|thousand|lakh|lac|rupees?|inr)\b", text_lower):
        return True
    # Plain number that looks like budget (e.g. 50000)
    if re.search(r"\b(\d{4,6})\b", original.replace(",", "")):
        # Could be budget if context suggests (e.g. "50,000" near "trip")
        if "budget" in text_lower or "rupee" in text_lower or "inr" in text_lower or "₹" in original or "rs" in text_lower:
            return True
        if re.search(r"\d+\s*(day|night)", text_lower) and re.search(r"\b\d{4,}\b", original.replace(",", "")):
            return True
    return False
