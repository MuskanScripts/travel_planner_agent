"""
Root Agent (Orchestrator) for the Smart Travel Planner.
Handles greeting/incomplete requests without sub-agents; triggers pipeline only when
destination, days/dates, and budget are present.
"""
# Load env before any Gemini/API usage (config loads dotenv)
from travel_planner import config  # noqa: F401

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import agent_tool

from travel_planner.sub_agents import (
    accommodation_agent,
    attraction_agent,
    itinerary_agent,
    transport_agent,
)
from travel_planner.tools import get_travel_intent

# Sequential pipeline: Attraction → Accommodation → Transport → Itinerary
# Invoked only when the user request is complete (has destination, days, budget).
travel_planner_pipeline = SequentialAgent(
    name="TravelPlannerPipeline",
    description="Generates full travel plan: attractions, accommodation, transport, budget allocation, day-by-day itinerary. Call this only when the user has provided destination, number of days (or dates), and budget.",
    sub_agents=[
        attraction_agent,
        accommodation_agent,
        transport_agent,
        itinerary_agent,
    ],
)

pipeline_tool = agent_tool.AgentTool(agent=travel_planner_pipeline)

# Root agent: intent detection first, then respond or run pipeline
root_agent = LlmAgent(
    name="TravelPlannerRootAgent",
    model=config.GEMINI_MODEL,
    description="Smart Travel Planner. Handles greetings and incomplete requests; generates full travel plans when destination, dates, and budget are provided.",
    instruction="""You are the Smart Travel Planner. Follow these rules strictly.

**Step 1 – Always call the tool first**
Call get_travel_intent with the user's latest message (the last thing the user said in this conversation). Use that tool result to decide what to do next.

**Step 2 – Act based on intent**
- If the tool returns intent "greeting": Respond with exactly the text in greeting_response. Do NOT call any other tool. Be brief and friendly.
- If the tool returns intent "incomplete": Respond by asking the user for the missing information. Use missing_fields and clarifying_suggestion from the tool result. Do NOT call the travel planning pipeline. Ask one short, polite message.
- If the tool returns intent "complete": Call the TravelPlannerPipeline tool (the travel planning pipeline) so it can generate the full plan. Do not summarize or reply before calling it; let the pipeline run and then its output will be the response.

**Required fields for "complete"**
The pipeline may only be run when the user has provided: destination, number of days or travel dates, and budget. If any of these are missing, treat as incomplete and ask for them.

**Do not**
- Do not call the pipeline for greetings (e.g. Hi, Hello, Hey, Good evening).
- Do not call the pipeline when the request is incomplete (e.g. "Plan a trip", "Goa trip" without days and budget).
- Do not skip calling get_travel_intent; always use it first with the user's message.""",
    tools=[get_travel_intent, pipeline_tool],
)
