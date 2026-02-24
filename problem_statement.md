# Smart Travel Planner Agent

## Title
Smart Travel Planner (Multi-Agent System using Google ADK)

## Problem

Design a multi-agent travel planning system that:

- **Accepts**: destination, travel dates, budget, and preferences (e.g. luxury, adventure, culture, budget-friendly).
- **Uses** Google Search to find attractions.
- **Estimates** hotel costs and transport costs.
- **Suggests** experiences and allocates budget smartly.
- **Generates** a structured day-by-day itinerary.

The system must demonstrate **orchestration between multiple agents**: a root orchestrator runs sub-agents in sequence (Attraction → Accommodation → Transport → Budget/Itinerary), with each agent using appropriate tools and passing results via shared state to produce a single, formatted travel plan.

## Success Criteria

- User provides a natural-language request (e.g. “Plan a 4-day trip to Goa with ₹50,000 budget, prefer adventure and beaches”).
- Output includes: **Estimated Costs Breakdown**, **Top Attractions**, **Budget Allocation**, and **Day-by-Day Itinerary**.
- Built-in **google_search** is used for attractions; custom tools handle hotel estimate, transport estimate, budget allocation, and itinerary generation.
- No API keys in code; configuration via `.env` and `python-dotenv`.
