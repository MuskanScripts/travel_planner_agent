# Smart Travel Planner (Multi-Agent System using Google ADK)

A production-ready multi-agent travel planning system built with **Google ADK (Python)**. It accepts destination, dates, budget, and preferences, then uses a pipeline of specialized agents to produce a structured travel plan with cost estimates, top attractions, budget allocation, and a day-by-day itinerary.

## Architecture (short)

The **root agent** is an **LlmAgent** that first runs **rule-based intent detection** (greeting vs incomplete vs complete). For **greetings** (e.g. "Hi", "Hello", "Good evening") it replies with a short welcome and asks for travel details without running sub-agents. For **incomplete requests** (e.g. "Plan a trip", "Goa trip") it asks clarifying questions for missing destination, days/dates, or budget. Only when **destination, days/dates, and budget** are present does it call the **TravelPlannerPipeline** (a SequentialAgent) that runs four sub-agents in order: **AttractionAgent** (Google Search), **AccommodationAgent**, **TransportAgent**, and **ItineraryAgent**, producing the full plan. All agents use **gemini-2.5-flash** and the built-in **google_search** in AttractionAgent.

## Project structure

```
travel_planner_agent/
├── travel_planner/
│   ├── __init__.py
│   ├── agent.py              # Root Agent (intent + pipeline orchestration)
│   ├── config.py             # Model and env (GOOGLE_API_KEY from .env)
│   ├── sub_agents/
│   │   ├── __init__.py
│   │   ├── attraction_agent.py
│   │   ├── accommodation_agent.py
│   │   ├── transport_agent.py
│   │   └── itinerary_agent.py
│   └── tools/
│       ├── __init__.py
│       ├── hotel_cost_estimator.py
│       ├── transport_cost_estimator.py
│       ├── budget_allocator.py
│       ├── itinerary_generator.py
│       └── travel_intent.py   # Rule-based greeting/incomplete/complete detection
├── problem_statement.md
├── README.md
├── requirements.txt
├── .env                     # You create this; add GOOGLE_API_KEY
└── .gitignore
```

## Setup

1. **Create and activate a virtual environment**

   Use the same command you used to check the version (`python` or `python3`):

   ```bash
   python -m venv .venv
   ```
   or, if only `python3` works on your system:
   ```bash
   python3 -m venv .venv
   ```

   Then activate it:
   - **Mac/Linux:** `source .venv/bin/activate`
   - **Windows (CMD):** `.venv\Scripts\activate.bat`
   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key**

   - Go to [Google AI Studio](https://aistudio.google.com/) and create an API key.
   - In the project root, create a `.env` file and add:

   ```
   GOOGLE_API_KEY=your_key_here
   ```

   Do not commit `.env`; it is listed in `.gitignore`.

## How to run

From the **project root** (`travel_planner_agent/`):

**CLI (interactive chat):**

```bash
adk run travel_planner
```

**Web UI (development only):**

```bash
adk web
```

Then open the URL shown (e.g. `http://localhost:8000`), select the agent **TravelPlannerRootAgent** (or the travel_planner agent) in the dropdown, and type your request.

## Example

**User input:**  
"Plan a 4-day trip to Goa with ₹50,000 budget, prefer adventure and beaches"

**Output (summary):**  
The system returns a formatted plan including:

- **Estimated Costs Breakdown** (hotel + transport)
- **Top Attractions** (from Google Search)
- **Budget Allocation** (remaining budget, activities, food)
- **Day-by-Day Itinerary**

## Requirements

- Python 3.10 or 3.11 (recommended: 3.11). Do not use 3.12+.
- `google-adk`, `python-dotenv` (see `requirements.txt`).

## Check if Python is installed

Before setup, verify you have Python and that it’s the right version:

1. **Open a terminal** (Command Prompt, PowerShell, or Terminal app).

2. **Check if Python is installed and which version:**
   ```bash
   python --version
   ```
   or:
   ```bash
   python3 --version
   ```

3. **Interpret the output:**
   - You should see something like `Python 3.10.x` or `Python 3.11.x`. **3.10 or 3.11 is required** for this project.
   - If you see `Python 2.x` or no command found, use `python3 --version` instead; on some systems `python` points to Python 2.
   - If the version is **3.12 or higher**, create a virtual environment using 3.10 or 3.11 if you have it (e.g. `py -3.11 -m venv .venv` on Windows, or install 3.11 and use `python3.11 -m venv .venv`).

4. **If Python is not installed:**
   - **Windows:** Install from [python.org](https://www.python.org/downloads/) and tick “Add Python to PATH”.
   - **macOS:** Install via [python.org](https://www.python.org/downloads/) or Homebrew: `brew install python@3.11`.
   - **Linux:** Use your package manager, e.g. `sudo apt install python3.11` (Ubuntu/Debian) or `sudo dnf install python3.11` (Fedora).

After you see `Python 3.10.x` or `Python 3.11.x`, continue with **Setup** below.
