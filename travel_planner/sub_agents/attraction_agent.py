"""
Attraction sub-agent: finds top attractions using Google Search.
"""
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from travel_planner.config import GEMINI_MODEL

attraction_agent = LlmAgent(
    name="AttractionAgent",
    model=GEMINI_MODEL,
    description="Finds top attractions for a destination using web search.",
    instruction="""You are a travel attractions expert.
From the user's message, identify: destination, number of days, budget (as a number), and preferences (e.g. adventure, beaches, culture, budget-friendly).
Use the google_search tool to find top attractions, things to do, and must-see places for that destination. Search for current, relevant results.
Then produce a single structured response in this format (use clear labels so the next agent can parse):
- Destination: <city/region>
- Days: <number>
- Budget: <number> (in INR if not specified)
- Preferences: <summary>
- Top Attractions: <numbered or bullet list of attraction names and short description>

Output only this structured summary. Be concise. List at least 5–8 attractions.""",
    tools=[google_search],
    output_key="attractions_result",
)
