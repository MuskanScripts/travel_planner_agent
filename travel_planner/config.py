"""
Configuration for the Smart Travel Planner agent.
Loads environment variables; never exposes API key in code.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini model - stable only (no -exp). Use 1.5-flash or 1.5-pro.
GEMINI_MODEL = "gemini-2.5-flash"

# API key loaded from .env; never hardcode
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
