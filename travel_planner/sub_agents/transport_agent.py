"""
Transport sub-agent: estimates transport cost using custom tool.
"""
from google.adk.agents import LlmAgent

from travel_planner.config import GEMINI_MODEL
from travel_planner.tools import transport_cost_estimator

transport_agent = LlmAgent(
    name="TransportAgent",
    model=GEMINI_MODEL,
    description="Estimates flight and local transport cost.",
    instruction="""You are a transport expert.
Use the previous outputs to get destination. The user may have mentioned an origin city; if not, assume a common origin like "Mumbai" for Indian destinations.

Previous step (attractions) mentioned destination:
{attractions_result}

Extract the destination. Use origin="Mumbai" (or the user's origin if clearly stated). Call transport_cost_estimator(origin=<origin>, destination=<destination>).
Summarize the transport estimate: flights and local transport, total in INR.""",
    tools=[transport_cost_estimator],
    output_key="transport_estimate",
)
