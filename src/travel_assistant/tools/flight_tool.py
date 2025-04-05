# src/travel_assistant/tools/flight_tool.py
from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
import os
from datetime import datetime

class FlightToolInput(BaseModel):
    origin: str = Field(..., description="Origin airport code or city.")
    destination: str = Field(..., description="Destination airport code or city.")
    departure_date: str = Field(..., description="Departure date in YYYY-MM-DD format.")
    return_date: Optional[str] = Field(None, description="Return date in YYYY-MM-DD format for round trips.")
    num_passengers: int = Field(1, description="Number of passengers.")
    max_results: int = Field(5, description="Maximum number of flight options to return.")

class FlightSearchTool(BaseTool):
    name: str = "FlightSearch"
    description: str = (
        "Search for flights between specified origins and destinations. "
        "Provides information on airlines, prices, duration, and layovers."
    )
    args_schema: Type[BaseModel] = FlightToolInput

    def _run(
        self, 
        origin: str, 
        destination: str, 
        departure_date: str, 
        return_date: Optional[str] = None, 
        num_passengers: int = 1,
        max_results: int = 3
    ) -> str:
        api_key = os.getenv("FLIGHT_API_KEY")
        api_secret = os.getenv("FLIGHT_API_SECRET")

        if not api_key or not api_secret:
            return "❌ Error: Missing Amadeus API credentials (FLIGHT_API_KEY or FLIGHT_API_SECRET)."

        try:
            access_token = self._get_amadeus_token(api_key, api_secret)
            response = self._call_amadeus_flights(
                access_token, origin, destination, departure_date, num_passengers, max_results
            )
            return self._format_flight_results(response, max_results)
        except Exception as e:
            return f"❌ Error fetching flight data: {str(e)}"

    def _get_amadeus_token(self, api_key: str, api_secret: str) -> str:
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        payload = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": api_secret,
        }
        res = requests.post(url, data=payload, headers=headers)
        res.raise_for_status()
        return res.json()["access_token"]

    def _call_amadeus_flights(self, token, origin, destination, departure_date, num_passengers, max_results):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = { "Authorization": f"Bearer {token}" }
        params = {
            "originLocationCode": origin.upper(),
            "destinationLocationCode": destination.upper(),
            "departureDate": departure_date,
            "adults": num_passengers,
            "max": max_results,
        }
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        return res.json()

    def _format_flight_results(self, data: dict, max_results: int = 3) -> str:
        offers = data.get("data", [])[:max_results]
        carriers = data.get("dictionaries", {}).get("carriers", {})
        aircrafts = data.get("dictionaries", {}).get("aircraft", {})

        if not offers:
            return "No flight offers found."

        output = "# ✈️ Available Flight Options\n\n"

        for idx, offer in enumerate(offers, 1):
            price = offer["price"]["grandTotal"]
            currency = offer["price"]["currency"]
            seats = offer.get("numberOfBookableSeats", "N/A")
            output += f"## Option {idx}: {price} {currency} ({seats} seats available)\n"

            for itin_idx, itinerary in enumerate(offer["itineraries"], 1):
                output += f"\n### Itinerary {itin_idx} - Duration: {itinerary['duration'].replace('PT', '')}\n"
                for seg in itinerary["segments"]:
                    dep = seg["departure"]
                    arr = seg["arrival"]
                    airline = carriers.get(seg["carrierCode"], seg["carrierCode"])
                    aircraft = aircrafts.get(seg["aircraft"]["code"], seg["aircraft"]["code"])
                    dep_time = dep["at"].replace("T", " ")
                    arr_time = arr["at"].replace("T", " ")
                    output += (
                        f"- **{airline} {seg['carrierCode']}{seg['number']}**: "
                        f"{dep['iataCode']} ({dep_time}) → {arr['iataCode']} ({arr_time})\n"
                        f"  - Duration: {seg['duration'].replace('PT', '')}\n"
                        f"  - Aircraft: {aircraft}\n"
                    )

            output += "\n---\n"

        return output
