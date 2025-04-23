## https://serper.dev/

from dotenv import load_dotenv
load_dotenv()
import os
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

from crewai_tools import SerperDevTool

# Initialize the tool for internet searching capabilities
search_tool = SerperDevTool()

class LocationInput(BaseModel):
    """Input for location suggestion."""
    description: str = Field(..., description="Description of the desired location")

class LocationSuggestionTool(BaseTool):
    name = "location_suggestion"
    description = "Suggests locations based on user description and preferences"
    args_schema: Type[BaseModel] = LocationInput

    def _run(self, description: str) -> str:
        """Return 5 static location suggestions regardless of the description."""
        static_locations = [
            {
                "title": "Paris, France",
                "snippet": "The City of Light offers iconic landmarks like the Eiffel Tower, world-class museums, and charming cafes. Perfect for art lovers and romantics."
            },
            {
                "title": "Kyoto, Japan",
                "snippet": "Ancient temples, traditional gardens, and stunning architecture showcase Japan's rich cultural heritage and peaceful atmosphere."
            },
            {
                "title": "Machu Picchu, Peru",
                "snippet": "This ancient Incan citadel set high in the Andes Mountains offers breathtaking views and fascinating historical significance."
            },
            {
                "title": "Santorini, Greece",
                "snippet": "Beautiful white-washed buildings, stunning sunsets over the Aegean Sea, and charming villages make this island a perfect Mediterranean getaway."
            },
            {
                "title": "Cape Town, South Africa",
                "snippet": "Combining stunning natural beauty, vibrant culture, and rich history with attractions like Table Mountain and beautiful beaches."
            }
        ]
        
        suggestions = []
        for location in static_locations:
            suggestions.append(f"- {location['title']}\n  {location['snippet']}")
        
        return "Here are some suggested locations based on your description:\n\n" + "\n\n".join(suggestions)

    def _arun(self, description: str) -> str:
        raise NotImplementedError("Async version not implemented")

# Initialize the location suggestion tool
location_tool = LocationSuggestionTool()