"""
Accommodation sub-agent: estimates hotel cost using custom tool.
"""
from google.adk.agents import LlmAgent

from travel_planner.config import GEMINI_MODEL
from travel_planner.tools import hotel_cost_estimator

accommodation_agent = LlmAgent(
    name="AccommodationAgent",
    model=GEMINI_MODEL,
    description="Estimates accommodation cost for the trip.",
    instruction="""You are an accommodation expert.
Use the output from the previous step (attractions_result) to get: destination (city), number of days, and budget.

Previous step output:
{attractions_result}

Extract the destination city, days, and budget (as a number in INR). If budget is not clearly in INR, assume INR.
Call the hotel_cost_estimator tool with: city=<destination>, days=<days>, budget=<total budget>.
Then summarize the accommodation estimate in one short paragraph: tier, per-night and total cost in INR.""",
    tools=[hotel_cost_estimator],
    output_key="hotel_estimate",
)
