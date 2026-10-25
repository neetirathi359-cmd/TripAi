from bson import ObjectId
from config.database import trips_collection

class TripModel:
    @staticmethod
    async def create_trip(trip_data: dict) -> dict:
        """Insert a new trip into the database and return the inserted document."""
        result = await trips_collection.insert_one(trip_data)
        trip_data["id"] = str(result.inserted_id)
        trip_data["userId"] = str(trip_data["userId"])
        if "_id" in trip_data:
            del trip_data["_id"]
        return trip_data

    @staticmethod
    async def get_trips_by_user(user_id: str) -> list:
        """Fetch all trips belonging to a specific user, sorted newest first."""
        cursor = trips_collection.find({"userId": ObjectId(user_id)}).sort("_id", -1)
        trips = []
        async for trip in cursor:
            trip["id"] = str(trip["_id"])
            trip["userId"] = str(trip["userId"])
            del trip["_id"]
            trips.append(trip)
        return trips

    @staticmethod
    async def get_trip_by_id(trip_id: str, user_id: str) -> dict | None:
        """Fetch a specific trip by trip ID and user ID."""
        try:
            trip = await trips_collection.find_one({
                "_id": ObjectId(trip_id),
                "userId": ObjectId(user_id)
            })
            if trip:
                trip["id"] = str(trip["_id"])
                trip["userId"] = str(trip["userId"])
                del trip["_id"]
                return trip
        except Exception:
            return None
        return None