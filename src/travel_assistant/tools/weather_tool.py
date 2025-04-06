# src/travel_assistant/tools/weather_tool.py
from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
import os
from datetime import datetime

class WeatherToolInput(BaseModel):
    """Input schema for OpenWeatherMapTool."""
    location: str = Field(..., description="The city or location to get weather for.")
    start_date: Optional[str] = Field(None, description="Start date in YYYY-MM-DD format.")
    end_date: Optional[str] = Field(None, description="End date in YYYY-MM-DD format.")

class OpenWeatherMapTool(BaseTool):
    name: str = "OpenWeatherMap"
    description: str = (
        "Get weather forecasts for a specific location during a date range. "
        "Provides temperature, conditions, and packing recommendations."
    )
    args_schema: Type[BaseModel] = WeatherToolInput

    def _run(self, location: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """Run the weather forecast tool"""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: OpenWeatherMap API key not found in environment variables"
        
        # Get coordinates for the location
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        
        if geo_response.status_code != 200 or not geo_response.json():
            return f"Could not find coordinates for {location}"
        
        # Extract coordinates
        location_data = geo_response.json()[0]
        lat = location_data['lat']
        lon = location_data['lon']
        
        # Get the forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        forecast_response = requests.get(forecast_url)
        
        if forecast_response.status_code != 200:
            return f"Error retrieving forecast"
        
        forecast_data = forecast_response.json()
        
        # Format the data into a simple response
        result = f"# Weather Forecast for {location_data['name']}\n\n"
        
        processed_days = set()
        
        for item in forecast_data['list']:
            # Convert timestamp to date
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime("%Y-%m-%d")
            
            # Only process each day once
            if date_str in processed_days:
                continue
                
            processed_days.add(date_str)
            
            # Add daily forecast
            result += f"## {dt.strftime('%A, %B %d')}\n\n"
            result += f"**Temperature**: {item['main']['temp_min']:.1f}°C to {item['main']['temp_max']:.1f}°C\n\n"
            result += f"**Conditions**: {item['weather'][0]['description']}\n\n"
            
            # Stop after processing 5 days 
            if len(processed_days) >= 5:
                break
        
        return result