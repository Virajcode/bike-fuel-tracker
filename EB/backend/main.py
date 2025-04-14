import time
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel

app = FastAPI(title="Locations API", description="API providing locations coordinates data")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CityRequest(BaseModel):
    input_string: str

@app.post("/locations", response_model=List[Dict[str, Any]])
async def get_cities(request: CityRequest = Body(...)):
    """
    Returns a list of major cities with their coordinates.
    
    Takes a long string as input but returns the same cities data regardless of input.
    The input string is received but not used in the response processing.
    """
    # Log or process the input_string if needed
    print(f"Received input string: {request.input_string[:100]}...")  # Print first 100 chars
    time.sleep(5)
    return [
        {
            "name": "New York City, USA",
            "place_id": "ChIJDT9zq3C_wjsRowiS4TAMzRs"
        },
        {
            "name": "London, UK",
            "place_id": "ChIJv6OzuEfBwjsRfsfW5Mjcf28"
        },
        {
            "name": "Tokyo, Japan",
            "place_id": "ChIJ41PwQ_LBwjsRypeqtFw7peY"
        },
        {
            "name": "Sydney, Australia",
            "place_id": "ChIJbYPmohLBwjsRvHK8CFQ6Kd8"
        },
        {
            "name": "Cape Town, South Africa",
            "place_id": "ChIJUWGRJTC_wjsR12dzhGAaM8c"
        }
    ]

@app.get("/")
async def root():
    """
    Root endpoint that provides information about the API.
    """
    return {
        "message": "Welcome to the locations API. Use POST /locations with a JSON body containing 'input_string' to get the list of locations."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)