# src/travel_assistant/chat_assistant.py
import os
from cerebras.cloud.sdk import Cerebras
from typing import Dict, Any

class ChatAssistant:
    """
    Chat assistant that can answer questions about a planned trip
    using the Cerebras API for LLM responses.
    """
    
    def __init__(self, trip_data: Dict[str, Any] = None):
        """
        Initialize the chat assistant with trip data.
        
        Args:
            trip_data: Dictionary containing all trip information
        """
        self.trip_data = trip_data or {}
        self.client = Cerebras(
            api_key=os.environ.get("CEREBRAS_API_KEY"),
        )
        self.chat_history = []

    def _format_system_prompt(self) -> str:
        """
        Create a system prompt with trip information to give context to the model.
        """
        # Extract key trip details for the system prompt
        origin = self.trip_data.get('origin', 'unknown origin')
        destination = self.trip_data.get('destination', 'unknown destination')
        departure_date = self.trip_data.get('departure_date', 'unknown departure date')
        return_date = self.trip_data.get('return_date', 'unknown return date')
        num_travelers = self.trip_data.get('num_travelers', 1)
        budget = self.trip_data.get('budget', 'unknown budget')
        
        # Get trip content if available
        itinerary = self._get_file_content('output/itinerary.md')
        weather = self._get_file_content('output/weather.md')
        flights = self._get_file_content('output/flights.md')
        hotels = self._get_file_content('output/hotels.md')
        
        # Create the system prompt
        system_prompt = f"""You are a helpful AI Travel Assistant. You've helped plan a trip with the following details:
- Origin: {origin}
- Destination: {destination}
- Departure Date: {departure_date}
- Return Date: {return_date}
- Number of Travelers: {num_travelers}
- Budget: ${budget}

You have access to the following information about the trip:

# ITINERARY:
{itinerary if itinerary else "Itinerary information not available."}

# WEATHER:
{weather if weather else "Weather information not available."}

# FLIGHTS:
{flights if flights else "Flight information not available."}

# HOTELS:
{hotels if hotels else "Hotel information not available."}

Answer the user's questions about their trip based on this information. If you don't know something or if it wasn't included in the plan, kindly let the user know and offer to help with something else related to their trip. Be friendly, helpful, and concise.
"""
        return system_prompt

    def _get_file_content(self, filepath: str) -> str:
        """Get content from a file if it exists."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
        return ""

    def get_response(self, user_message: str) -> str:
        """
        Get a response from the chat assistant based on user's message.
        
        Args:
            user_message: The message from the user
            
        Returns:
            str: The assistant's response
        """
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": user_message})
        
        # Prepare messages for the API call
        messages = [
            {"role": "system", "content": self._format_system_prompt()},
        ]
        # Add chat history (limited to last 10 messages to avoid token limits)
        messages.extend(self.chat_history[-10:])
        
        # Make the API call
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama3.3-70b",  # Using the same model as the agents
                temperature=0.7,
                max_tokens=1024
            )
            
            # Extract the response
            response = chat_completion.choices[0].message.content
            
            # Add assistant response to chat history
            self.chat_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg