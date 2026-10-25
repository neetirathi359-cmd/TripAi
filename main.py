from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, trips

app = FastAPI(title="TripAI Backend", version="1.0.0")

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(trips.router)

@app.get("/")
def root():
    return {"message": "Welcome to TripAI API. Visit /docs for documentation."}