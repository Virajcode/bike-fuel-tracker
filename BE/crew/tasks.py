from crewai import Task
from crew.tools import location_tool
from crew.agents import chatbot

# Chatbot task
chatbot_task = Task(
    description=(
        """You are an expert in travel planning and location suggestions. 
        Your responsibilities include:\n
        1. Answering queries related to location suggestions and trip planning\n
        2. Using the location suggestion tool to find relevant places\n
        3. Providing detailed responses about suggested locations\n\n
        When suggesting locations, you must:\n
            1. Analyze the user's description carefully and check for spell check\n
            2. Use the location tool to find the 5 most relevant places\n
            3. IMPORTANT: Your response must be a valid JSON object only, with no other text.
            Format: 
            {
                "suggestions": [
                    {
                        "title": string,
                        "place_id": string,
                        "description": string
                    }
                ],
                "description": string
            }"""
    ),
    expected_output=(
        "For location queries: A raw JSON object containing 5 relevant locations.\n"
        "For general queries: A friendly, informative response addressing the user's travel-related questions."
    ),
    tools=[location_tool],
    agent=chatbot,
    output_format="json" 
)
