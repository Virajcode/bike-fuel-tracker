from crewai import Agent, Task, Crew
from crewai import tools as crew_tools
from crew.agents import chatbot
from crew.tasks import chatbot_task


# Initialize conversation history
conversation_history = []

# from crewai import Crew

# Create the crew with your agents
assistant_crew = Crew(
    agents=[chatbot],
    tasks=[],  # Initialize with empty tasks list
    verbose=2
)

import json
import re

def parse_llm_response_to_json(response):
    """
    Extract and parse JSON from LLM responses regardless of formatting.
    """
    # First try: Look for content between json code blocks
    try:
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
        if json_match:
            return json.loads(json_match.group(1))
    except:
        pass
    
    # Second try: Look for anything that might be a JSON object
    try:
        json_match = re.search(r'(\{[\s\S]*\})', response)
        if json_match:
            return json.loads(json_match.group(1))
    except:
        pass
    
    # Third try: Just attempt to parse the entire response
    try:
        return json.loads(response)
    except:
        return "flase"




def process_user_query(user_input):
    # Add user input to conversation history
    conversation_history.append(f"User: {user_input}")
    
    # Create a task with conversation context
    context = "\n".join(conversation_history[-5:])  # Include last 5 exchanges for context
    query_task = Task(
        # description=f"Process and respond to: '{user_input}'\nPrevious conversation context:\n{context}",
        # expected_output="A helpful response that addresses the user's needs",
        agent=chatbot,
        
        description=(
            f"""Process and respond to: '{user_input}'\nPrevious conversation context:\n{context}
            You are an expert in travel planning and location suggestions. 
            Your responsibilities include:\n
            1. Answering queries related to location suggestions and trip planning\n
            2. Using the location suggestion tool to find relevant places\n
            3. Providing detailed responses about suggested locations\n\n
            When suggesting locations, you must:\n
                1. Analyze the user's description carefully and check for spell check\n
                2. Use the location tool to find the 5 most relevant places\n
                3. IMPORTANT: Your response must be a valid JSON object only, with no other text For location queries only."""
        ),
        expected_output=(
            "For location queries: A raw **JSON** object containing 5 relevant locations.do not give type as text i only want json\n"
            "For general queries: A friendly, informative response addressing the user's travel-related questions."
        ),
    )
    
    # Set the task and run the crew
    assistant_crew.tasks = [query_task]
    result = assistant_crew.kickoff()
    json_data = parse_llm_response_to_json(result)
    if json_data == "flase":
        # Add response to conversation history
        conversation_history.append(f"Assistant: {result}")
        return result
    else:
        # Add response to conversation history
        conversation_history.append(f"Assistant: {json_data}")
        return json_data