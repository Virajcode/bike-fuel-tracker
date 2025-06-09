import time
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel
# import uvicorn
# from get_locations import get_location
from crew.chatbot import process_user_query
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

    
@app.post("/locations")
async def get_cities(request: CityRequest = Body(...)):
    """
    Returns cities data or a string based on the processed query.
    
    Takes a long string as input. The response type can be either:
    - A list of dictionaries with city information
    - A string response
    """
    try:
        # Log or process the input_string if needed
        print(f"Received input string: {request.input_string[:100]}...")  # Print first 100 chars
        
        # Get the response
        result = process_user_query(request.input_string)
        
        # Check the type of result and return appropriate response
        if isinstance(result, str):
            return {"type": "text", "content": result}
        elif isinstance(result, (list, dict)):
            return {"type": "json", "content": result}
        else:
            return {"type": "error", "content": "Unexpected response type"}
        # return [{'rank': 1, 'score': 1.221296787261963, 'index': 11, 'title': 'Aditya Shagun Mall', 'place_id': 'ChIJL9wRPVm-wjsRcD1BYTfcW_E'}, {'rank': 2, 'score': 1.247261881828308, 'index': 6, 'title': 'Royale Heritage Mall', 'place_id': 'ChIJndd_RLvrwjsRx5LWxbkYYH8'}, {'rank': 3, 'score': 1.3079421520233154, 'index': 21, 'title': 'ISKCON NVCC Pune', 'place_id': 'ChIJSdctqfvqwjsR7tcJvlsbul4'}, {'rank': 4, 'score': 1.314194917678833, 'index': 15, 'title': 'Piazza Pizza By Little Italy SGS Mall', 'place_id': 'ChIJ0wMQ-U_AwjsRsuEOeqz4KPc'}, {'rank': 5, 'score': 1.3251968622207642, 'index': 2, 'title': 'Seasons Mall', 'place_id': 'ChIJ41PwQ_LBwjsRypeqtFw7peY'}]
            
    except Exception as e:
        return {"type": "error", "content": str(e)}


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