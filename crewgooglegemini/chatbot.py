from crewai import Agent, Task, Crew
from crewai import tools as crew_tools
from agents import chatbot


# Initialize conversation history
conversation_history = []

# from crewai import Crew

# Create the crew with your agents
assistant_crew = Crew(
    agents=[chatbot],
    tasks=[],  # Initialize with empty tasks list
    verbose=2
)



def process_user_query(user_input):
    # Add user input to conversation history
    conversation_history.append(f"User: {user_input}")
    
    # Create a task with conversation context
    context = "\n".join(conversation_history[-5:])  # Include last 5 exchanges for context
    query_task = Task(
        description=f"Process and respond to: '{user_input}'\nPrevious conversation context:\n{context}",
        expected_output="A helpful response that addresses the user's needs",
        agent=chatbot
    )
    
    # Set the task and run the crew
    assistant_crew.tasks = [query_task]
    result = assistant_crew.kickoff()
    
    # Add response to conversation history
    conversation_history.append(f"Assistant: {result}")
    return result

# Simple chat loop
def chat_interface():
    print("Chatbot: Hello! How can I help you today?")
    conversation_history.append("Assistant: Hello! How can I help you today?")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            conversation_history.append("Assistant: Goodbye!")
            break
            
        response = process_user_query(user_input)
        print(f"Chatbot: {response}")

# Start the chat
if __name__ == "__main__": 
    chat_interface()