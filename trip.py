import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

from config.database import trips_collection
from schemas.trip_schema import TripRequest
from models.user_model import get_current_user

router = APIRouter(prefix="/api/trips", tags=["Trips"])

ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_trip(trip_req: TripRequest, current_user: dict = Depends(get_current_user)):
    try:
        prompt = f"""
        Create a detailed {trip_req.duration}-day travel itinerary for {trip_req.travelers} traveler(s) visiting {trip_req.destination}.
        Budget level: {trip_req.budget}. Traveler interests: {', '.join(trip_req.interests)}.
        
        Return ONLY valid JSON with this exact structure:
        {{
          "tripTitle": "Title of the trip",
          "summary": "Short description",
          "days": [
            {{
              "dayNumber": 1,
              "title": "Day theme or title",
              "highlights": ["activity 1", "activity 2"],
              "schedule": {{
                "morning": "...",
                "afternoon": "...",
                "evening": "..."
              }}
            }}
          ]
        }}
        """

        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        itinerary_data = json.loads(response.text)

        trip_doc = {
            "userId": ObjectId(current_user["id"]),
            "destination": trip_req.destination,
            "duration": trip_req.duration,
            "travelers": trip_req.travelers,
            "budget": trip_req.budget,
            "interests": trip_req.interests,
            "itinerary": itinerary_data
        }

        result = await trips_collection.insert_one(trip_doc)
        trip_doc["id"] = str(result.inserted_id)
        trip_doc["userId"] = str(trip_doc["userId"])
        del trip_doc["_id"]

        return trip_doc

    except Exception as e:
        print(f"Error generating itinerary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate itinerary. Please try again.")

@router.get("/")
async def get_user_trips(current_user: dict = Depends(get_current_user)):
    cursor = trips_collection.find({"userId": ObjectId(current_user["id"])}).sort("_id", -1)
    trips = []
    async for trip in cursor:
        trip["id"] = str(trip["_id"])
        trip["userId"] = str(trip["userId"])
        del trip["_id"]
        trips.append(trip)
    return trips