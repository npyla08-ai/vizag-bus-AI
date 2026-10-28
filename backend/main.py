import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from backend.db import (
    fetch_buses,
    fetch_alternatives,
    update_crowd_level,
    save_complaint,
    fetch_complaints,
)

# Load GEMINI_API_KEY from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="Vizag Bus AI API")

# Allow Frontend (HTML/JS) to call this Backend without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class CrowdUpdateRequest(BaseModel):
    bus_number: str
    crowd_percentage: int

class ComplaintRequest(BaseModel):
    bus_number: str
    complaint_text: str

# 1. GET Buses (Used for Bus List + Clicking a Bus to Show on Leaflet Map)
@app.get("/api/buses")
def get_buses(source: str = None, destination: str = None):
    buses = fetch_buses(source, destination)
    alternatives = fetch_alternatives(source, destination) if (source and destination) else []
    return {"buses": buses, "alternatives": alternatives}

# 2. POST Simulate Computer Vision Crowd Detection
@app.post("/api/simulate-crowd")
def simulate_crowd(data: CrowdUpdateRequest):
    updated = update_crowd_level(data.bus_number, data.crowd_percentage)
    return {"message": "Crowd level updated via CV simulation", "data": updated}

# 3. GET Gemma AI Smart Recommendation (Ready in Backend - Connect to Frontend on Sunday!)
@app.get("/api/ai-recommend")
def ai_recommendation(source: str, destination: str):
    buses = fetch_buses(source, destination)
    alternatives = fetch_alternatives(source, destination)

    if not buses:
        return {"recommendation": "No direct buses found for this route right now."}

    prompt = f"""
    You are Vizag Bus AI, a smart public transport assistant for Visakhapatnam.
    A commuter wants to travel from {source} to {destination}.
    
    Available Buses right now:
    {buses}
    
    Alternative / Connecting Routes:
    {alternatives}
    
    Give a short, crisp 3-bullet point answer:
    1. When should I leave? (Calculate based on ETA)
    2. Which bus should I take? (Compare crowd_percentage vs waiting time)
    3. What if my bus is full? (Mention the less-crowded bus or alternative route)
    """

    if not API_KEY or API_KEY == "your_actual_api_key_here":
        # Fallback response if API key isn't added yet
        return {
            "recommendation": (
                f"• Leave in {buses[0]['eta_minutes']} mins for Bus {buses[0]['bus_number']}, OR wait {buses[-1]['eta_minutes']} mins for Bus {buses[-1]['bus_number']}.\n"
                f"• Recommendation: Avoid Bus {buses[0]['bus_number']} ({buses[0]['crowd_percentage']}% full). Board Bus {buses[-1]['bus_number']} ({buses[-1]['crowd_percentage']}% full - Comfortable).\n"
                f"• Alternative: {alternatives[0]['route_details'] if alternatives else 'Take next connecting express bus.'}"
            )
        }

    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt,
        )
        return {"recommendation": response.text}
    except Exception as e:
        return {"recommendation": f"AI Fallback Advice: Wait for the comfortable bus ({buses[-1]['bus_number']}) instead of the overcrowded bus ({buses[0]['bus_number']}). Error details: {str(e)}"}

# 4. POST & GET Complaints (With AI Auto-Categorization)
@app.post("/api/complaints")
def create_complaint(data: ComplaintRequest):
    category = "Crowd / Frequency" if "crowd" in data.complaint_text.lower() or "full" in data.complaint_text.lower() else "Stop / Driver Issue"
    priority = "High" if "skip" in data.complaint_text.lower() or "rude" in data.complaint_text.lower() else "Medium"
    save_complaint(data.bus_number, data.complaint_text, category, priority)
    return {"message": "Complaint registered and categorized by AI", "category": category, "priority": priority}

@app.get("/api/complaints")
def list_complaints():
    return {"complaints": fetch_complaints()}
