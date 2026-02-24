"""
Root Agent (Orchestrator) for the Smart Travel Planner.
Runs sub-agents sequentially: Attraction → Accommodation → Transport → Itinerary.
"""
# Load env before any Gemini/API usage (config loads dotenv)
from travel_planner import config  # noqa: F401

from google.adk.agents import LlmAgent, SequentialAgent

from travel_planner.sub_agents import (
    accommodation_agent,
    attraction_agent,
    itinerary_agent,
    transport_agent,
)

# Sequential pipeline: Attraction → Accommodation → Transport → Itinerary
# Each sub-agent writes to state via output_key; next agent reads via {key} in instruction.
travel_planner_pipeline = SequentialAgent(
    name="TravelPlannerRootAgent",
    description="Orchestrates travel planning: attractions, accommodation, transport, budget, itinerary.",
    sub_agents=[
        attraction_agent,
        accommodation_agent,
        transport_agent,
        itinerary_agent,
    ],
)

# ADK discovers root_agent from this module
root_agent = travel_planner_pipeline
