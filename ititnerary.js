
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function generateItinerary(trip) {
  const {
    destination,
    startDate,
    endDate,
    travelers,
    budget,
    interests
  } = trip;

  const prompt = `
Create a personalized travel itinerary.

Destination: ${destination}
Start Date: ${startDate}
End Date: ${endDate}
Number of Travelers: ${travelers}
Total Budget: ₹${budget}
Interests: ${interests}

Instructions:
1. Create a day-by-day travel itinerary.
2. Include places to visit and activities for each day.
3. Suggest suitable timings for each activity.
4. Include estimated food, transport and activity costs.
5. Match the user's interests and total budget.
6. Give practical travel tips.
7. Return the result as JSON in this format:

{
  "destination": "Destination name",
  "days": [
    {
      "day": 1,
      "activities": [
        {
          "time": "10:00 AM",
          "place": "Place name",
          "description": "Activity details",
          "estimatedCost": 500
        }
      ]
    }
  ],
  "estimatedTotalCost": 5000,
  "travelTips": ["Tip 1", "Tip 2"]
}
`;

  const response = await client.responses.create({
    model: "gpt-4.1-mini",
    instructions:
      "You are TripAI, an AI travel planner. Generate practical, personalized itineraries and return valid JSON only.",
    input: prompt,
    text: {
      format: { type: "json_object" }
    }
  });

  return JSON.parse(response.output_text);
}
