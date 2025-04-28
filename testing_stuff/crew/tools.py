## https://serper.dev/

from dotenv import load_dotenv
load_dotenv()
import os
from langchain.tools import BaseTool
from typing import Optional, Type, Dict, List
from pydantic import BaseModel, Field
from .get_locations import get_location

# Validate environment variables
if not os.getenv('SERPER_API_KEY'):
    raise ValueError("SERPER_API_KEY not found in environment variables")

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
from crewai_tools import SerperDevTool

class LocationInput(BaseModel):
    """Input schema for location suggestion."""
    description: str = Field(
        ..., 
        description="Description of the desired location",
        min_length=3,
        max_length=1000
    )

class LocationSuggestionTool(BaseTool):
    name = "location_suggestion"
    description = """
    Suggests locations based on user description and preferences.
    Returns up to 5 relevant locations in a structured format.
    Input should be a detailed description of the desired location or experience.
    """
    args_schema: Type[BaseModel] = LocationInput

    def _run(self, description: str) -> str:
        """
        Get location suggestions based on the description.
        
        Args:
            description (str): User's description of desired location
            
        Returns:
            str: JSON string containing suggested locations
            
        Raises:
            ValueError: If description is invalid or no locations found
        """
        if not description or len(description.strip()) < 3:
            raise ValueError("Description must be at least 3 characters long")
            
        try:
            suggested_locations = get_location(description)
            if not suggested_locations:
                return {"suggestions": [], "message": "No locations found matching your description"}
            # Return raw JSON without any markdown formatting
            return suggested_locations
        except Exception as e:
            raise RuntimeError(f"Error getting location suggestions: {str(e)}")

    def _arun(self, description: str) -> str:
        """Async version is not implemented."""
        raise NotImplementedError("Async version not implemented")

# Initialize tools
search_tool = SerperDevTool()
location_tool = LocationSuggestionTool()