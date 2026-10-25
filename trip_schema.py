from pydantic import BaseModel
from typing import List, Optional

class TripRequest(BaseModel):
    destination: str
    duration: int  # in days
    travelers: int
    budget: str
    interests: List[str]

class TripResponse(BaseModel):
    id: Optional[str] = None
    userId: str
    destination: str
    duration: int
    travelers: int
    budget: str
    interests: List[str]
    itinerary: dict