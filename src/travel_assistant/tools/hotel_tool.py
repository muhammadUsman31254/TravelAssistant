from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
import os
from datetime import datetime, timedelta
import json

class HotelToolInput(BaseModel):
    """Input schema for HotelSearchTool."""
    location: str = Field(..., description="City or location to search hotels.")
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format.")
    check_out_date: str = Field(..., description="Check-out date in YYYY-MM-DD format.")
    guests: int = Field(1, description="Number of guests.")
    budget_max: Optional[float] = Field(None, description="Maximum price per night in USD.")
    max_results: int = Field(5, description="Maximum number of hotel options to return.")

class HotelSearchTool(BaseTool):
    name: str = "HotelSearch"
    description: str = (
        "Search for hotels in a specified location. "
        "Provides information on prices, amenities, ratings, and availability."
    )
    args_schema: Type[BaseModel] = HotelToolInput

    def _run(
        self, 
        location: str, 
        check_in_date: str, 
        check_out_date: str, 
        guests: int = 1,
        budget_max: Optional[float] = None,
        max_results: int = 3
    ) -> str:
        """Run the hotel search tool"""
        api_key = os.getenv("HOTEL_API_KEY")
        if not api_key:
            return "Error: API key not found."
        
        # Make the API call to the hotel provider (Amadeus example)
        try:
            hotel_data = self._call_hotel_api(api_key, location, check_in_date, check_out_date, guests, budget_max, max_results)
            return hotel_data
        except Exception as e:
            return f"Error searching for hotels: {str(e)}"
    
    def _call_hotel_api(self, api_key: str, location: str, check_in_date: str, check_out_date: str, guests: int, budget_max: Optional[float], max_results: int) -> str:
        """Call the real hotel API to fetch available hotels"""
        
        # Define the endpoint URL (replace with actual endpoint of your API)
        url = f"https://test.api.amadeus.com/v2/shopping/hotels/by-city"
        
        # Define query parameters (you can modify these based on the API you're using)
        params = {
            "cityCode": location,
            "checkInDate": check_in_date,
            "checkOutDate": check_out_date,
            "adults": guests,
            "max": max_results,
            "currencyCode": "USD"  # You can modify this as per the API's requirement
        }

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        # Make the request to the Amadeus API (replace with actual endpoint of your API)
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return self._parse_hotel_data(response.json(), budget_max)
        else:
            return f"Error: {response.text}"

    def _parse_hotel_data(self, data: dict, budget_max: Optional[float]) -> str:
        """Parse the hotel data response"""
        if not data.get("data"):
            return "No hotels found for the given criteria."
        
        hotels = data["data"]
        result = "### Hotel Options\n\n"
        
        for hotel in hotels:
            hotel_name = hotel.get("name", "Unknown Hotel")
            distance = hotel.get("distance", {}).get("value", 0)
            country_code = hotel.get("address", {}).get("countryCode", "Unknown Country")
            
            # Example of filtering based on price (if price info was available in the API response)
            # You would filter based on price per night here if available in the response.
            # For now, we'll skip price filtering since the response doesn't contain it.

            result += f"**Hotel Name**: {hotel_name}\n"
            result += f"**Distance from city center**: {distance} km\n"
            result += f"**Country**: {country_code}\n"
            result += f"**Latitude**: {hotel.get('geoCode', {}).get('latitude', 'N/A')}\n"
            result += f"**Longitude**: {hotel.get('geoCode', {}).get('longitude', 'N/A')}\n\n"
        
        return result or "No hotels found within your budget."

