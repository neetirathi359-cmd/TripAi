require("dotenv").config();

const express = require("express");
const { GoogleGenAI } = require("@google/genai");

const app = express();
app.use(express.json());

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY
});

app.post("/api/itinerary", async (req, res) => {
  try {
    const {
      destination,
      startDate,
      endDate,
      duration,
      travelers,
      budget,
      interests
    } = req.body;

    if (!destination || !budget) {
      return res.status(400).json({
        error: "Destination and budget are required."
      });
    }

    const prompt = `
You are the AI travel planner for TripAI.

Create a practical travel itinerary using these details:
Destination: ${destination}
Start date: ${startDate || "Not provided"}
End date: ${endDate || "Not provided"}
Duration: ${duration || "Not provided"}
Travelers: ${travelers || 1}
Total budget: ${budget}
Interests: ${interests || "General sightseeing"}

Requirements:
1. Organize the itinerary day by day.
2. Suggest morning, afternoon and evening activities.
3. Consider the user's budget and interests.
4. Include estimated costs in the budget's currency, assumed to be INR.
5. Include food and local transport estimates where possible.
6. Clearly mention that prices and opening hours must be verified.
7. Do not claim that bookings or live availability have been verified.
8. Return a clear, useful itinerary.
`;

    const response = await ai.models.generateContent({
      model: "gemini-3.8-flash",
      contents: prompt
    });

    res.json({
      success: true,
      itinerary: response.text
    });

  } catch (error) {
    console.error("Gemini error:", error);

    res.status(500).json({
      success: false,
      error: "Could not generate itinerary. Please try again."
    });
  }
});

app.listen(3000, () => {
  console.log("TripAI AI server running at http://localhost:3000");
});