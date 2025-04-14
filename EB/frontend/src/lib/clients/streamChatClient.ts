import { Message, Location } from "@/lib/types";
import { generateUUID } from "@/lib/utils";
import { fetchEventSource } from "@microsoft/fetch-event-source";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const streamChat = async ({
  inputContent,
  setIsLoading,
  append,
}: {
  inputContent: string;
  setIsLoading: (isLoading: boolean) => void;
  append: (message: Message) => void;
}) => {
  try {
    setIsLoading(true);
    
    // Call the cities API using fetch
    const response = await fetch(`${apiUrl}/locations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ input_string: inputContent }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    // Parse the cities data from the response
    const locations: Location[] = await response.json();

    // Create a message with the locations data
    const content: Message = {
      id: generateUUID(),
      content: `Here are some major cities around the world:`,
      locations: locations, // Add the locations data from the API
      role: "assistant",
      parts: [{ 
        type: "text", 
        text: `Here are some major cities around the world. I processed your input: "${inputContent.substring(0, 50)}${inputContent.length > 50 ? '...' : ''}"` 
      }],
    };

    append(content);
    
  } catch (err) {
    console.log(`Error calling cities API. Details: ${err}`);
    
    // Create an error message
    const errorMessage: Message = {
      id: generateUUID(),
      content: `Sorry, there was an error fetching city data.`,
      role: "assistant",
      parts: [{ type: "text", text: `Sorry, there was an error fetching city data. Error: ${err}` }],
    };
    
    append(errorMessage);
  } finally {
    setIsLoading(false);
  }
};