from crewai import Agent
from crew.tools import location_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

# Verify API key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure LiteLLM for Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Create an agent that will serve as your chatbot
chatbot = Agent(
    role="Travel Planning Assistant",
    goal="""Help users plan trips and suggest locations based on their descriptions.
        When suggesting locations, analyze the user's description carefully and use the location tool
        to find the 5 most relevant places.And return the final answer as a valid JSON object.""",
    backstory="I'm an AI travel assistant specialized in suggesting personalized travel destinations and creating custom trip itineraries. I use advanced tools to find the perfect locations based on user preferences.",
    verbose=True,
    allow_delegation=False,
    tools=[location_tool],
    llm=llm,
    memory=True,
    system_message=""""strictly follow the instructions and provide a valid JSON object as output For location queries.
        Do not include any other text or markdown formatting in your response. 
        Your response should be a valid JSON object with the following format For location queries:
        {
            "suggestions": [
                {
                    "title": string,
                    "place_id": string,
                    "description": string
                }
            ],
            "description": string
        }
        Dont add any thing extra other than this JSON object.""",
    
)
