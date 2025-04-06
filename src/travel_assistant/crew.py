# src/travel_assistant/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from travel_assistant.tools.weather_tool import OpenWeatherMapTool
from travel_assistant.tools.flight_tool import FlightSearchTool
# from travel_assistant.tools.hotel_tool import HotelSearchTool

@CrewBase
class TravelAssistantCrew():
    """Travel Assistant crew for generating trip itineraries"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    @agent
    def travel_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_researcher'],
            verbose=True,
            tools=[SerperDevTool()],
            llm = LLM(
                model="cerebras/llama3.3-70b",
                temperature=0.7,
                max_tokens=10000
            )
        )

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_planner'],
            verbose=True,
            tools=[SerperDevTool()],
            llm = LLM(
                model="cerebras/llama3.3-70b",
                temperature=0.7,
                max_tokens=10000
            )
        )
    
    @agent
    def weather_forecaster(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_forecaster'],
            verbose=True,
            tools=[OpenWeatherMapTool()],
            llm = LLM(
                model="cerebras/llama3.3-70b",
                temperature=0.5,
                max_tokens=10000
            )
        )
    
    @agent
    def flight_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['flight_finder'],
            verbose=True,
            tools=[FlightSearchTool()],
            llm = LLM(
                model="cerebras/llama3.3-70b",
                temperature=0.6,
                max_tokens=10000
            )
        )
    
    @agent
    def hotel_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['hotel_finder'],
            verbose=True,
            # tools=[HotelSearchTool()],
            llm = LLM(
                model="cerebras/llama3.3-70b",
                temperature=0.6,
                max_tokens=10000
            )
        )

    @task
    def destination_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['destination_research_task'],
        )

    @task
    def itinerary_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_creation_task'],
            output_file='output/itinerary.md'  
        )
    
    @task
    def weather_forecast_task(self) -> Task:
        return Task(
            config=self.tasks_config['weather_forecast_task'],
            output_file='output/weather.md'  
        )
    
    @task
    def flight_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['flight_search_task'],
            output_file='output/flights.md'  
        )
    
    @task
    def hotel_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['hotel_search_task'],
            output_file='output/hotels.md'  
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Travel Assistant crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )