"""
Itinerary sub-agent: allocates budget and generates day-by-day itinerary.
"""
from google.adk.agents import LlmAgent

from travel_planner.config import GEMINI_MODEL
from travel_planner.tools import budget_allocator, itinerary_generator

itinerary_agent = LlmAgent(
    name="ItineraryAgent",
    model=GEMINI_MODEL,
    description="Allocates budget and creates day-by-day itinerary.",
    instruction="""You are an itinerary and budget expert.
You have three previous outputs:
1) Attractions: {attractions_result}
2) Hotel estimate: {hotel_estimate}
3) Transport estimate: {transport_estimate}

From these, extract: destination, days (number), total_budget (number in INR), hotel_cost (number), transport_cost (number), and a list of attraction names.

Step 1: Call budget_allocator(total_budget=..., hotel_cost=..., transport_cost=...) to get budget allocation.
Step 2: Call itinerary_generator(destination=..., attractions=[list of attraction names], days=...) to get the day-by-day plan.

Then produce the final travel plan in this exact structure:

## Estimated Costs Breakdown
<summary of hotel + transport from tools>

## Top Attractions
<list from attractions_result>

## Budget Allocation
<result from budget_allocator: remaining, activities, food>

## Day-by-Day Itinerary
<output from itinerary_generator, formatted clearly>

Output only this formatted plan. No extra preamble.""",
    tools=[budget_allocator, itinerary_generator],
    output_key="final_plan",
)
