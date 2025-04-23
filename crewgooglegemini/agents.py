from crewai import Agent
from tools import location_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

# Verify API key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure LiteLLM for Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Updated model name format
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Create an agent that will serve as your chatbot
chatbot = Agent(
    role="Personal Assistant Chatbot",
    goal="Help users by answering questions and performing tasks, especially providing location suggestions",
    backstory="I'm an AI assistant that can use various tools to help users, including suggesting travel destinations and places to visit.",
    verbose=True,
    allow_delegation=True,
    tools=[location_tool],
    llm=llm,
    memory=True  # Enable memory for conversation history
)
