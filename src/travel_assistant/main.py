# src/travel_assistant/main.py
import os
import warnings
import traceback
from dotenv import load_dotenv
import streamlit as st
from travel_assistant.crew import TravelAssistantCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Load environment variables
load_dotenv()

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

def main():
    st.set_page_config(
        page_title="AI Travel Assistant",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="auto"
    )

    st.header("✈️ AI Travel Assistant", divider="rainbow")

    # Sidebar for trip details
    with st.sidebar:
        st.header("🗺️ Plan Your Trip")
        origin = st.text_input("📍 Origin")
        destination = st.text_input("🌍 Destination")
        departure_date = st.date_input("🛫 Departure Date")
        return_date = st.date_input("🛬 Return Date")
        budget = st.slider("💰 Budget ($)", 0, 1000, 100, 50)
        num_travelers = st.number_input("👥 Number of Travelers", 1, 10, 1)
        
        plan_button = st.button("Plan My Trip", icon="🚀", use_container_width=True, type="primary")

    # Initialize session state
    if "planning_started" not in st.session_state:
        st.session_state.planning_started = False
        st.session_state.itinerary = None
        st.session_state.weather = None
        st.session_state.flights = None
        st.session_state.hotels = None

    # Display welcome message if planning hasn't started
    if not st.session_state.planning_started:
        st.markdown('### 🌟 What Our Assistant Can Do For You!')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('##### 📅 Itinerary Planning')
            st.markdown("Customized day-by-day plans for your destination")
        with col2:
            st.markdown("##### 🌤️ Weather Forecasts")
            st.markdown("Know what to pack with accurate weather data")
        with col3:
            st.markdown("##### ✈️ Flight Options")
            st.markdown("Find the best flight deals for your dates")
        with col4:
            st.markdown("##### 🏨 Hotel Suggestions")
            st.markdown("Accommodations that match your preferences")

    # When the button is clicked, save user inputs to session state
    if plan_button:

        st.session_state.planning_started = True
        st.session_state.origin = origin
        st.session_state.destination = destination
        st.session_state.departure_date = departure_date
        st.session_state.return_date = return_date
        st.session_state.budget = budget
        st.session_state.num_travelers = num_travelers

        # Run the AI Agents
        with st.spinner("🔃 Our AI agents are planning your perfect trip..."):
            try:
                # Calculate trip duration in days
                trip_duration = (return_date - departure_date).days
                
                # Initialize and run the crew
                inputs = {
                    'origin': origin,
                    'destination': destination,
                    'departure_date': departure_date.strftime('%Y-%m-%d'),
                    'return_date': return_date.strftime('%Y-%m-%d'),
                    'trip_duration': trip_duration,  
                    'budget': budget,
                    'num_travelers': num_travelers
                }
                
                # Run the crew
                TravelAssistantCrew().crew().kickoff(inputs=inputs)
                
                # Save
                if os.path.exists('output/itinerary.md'):
                    with open('output/itinerary.md', 'r') as f:
                        st.session_state.itinerary = f.read()
                    st.success("✅ Itinerary Planning!")

                if os.path.exists('output/weather.md'):
                    with open('output/weather.md', 'r') as f:
                        st.session_state.weather = f.read()
                    st.success("✅ Weather forecast!")
                
                if os.path.exists('output/flights.md'):
                    with open('output/flights.md', 'r') as f:
                        st.session_state.flights = f.read()
                    st.success("✅ Flight options!")
                
                if os.path.exists('output/hotels.md'):
                    with open('output/hotels.md', 'r') as f:
                        st.session_state.hotels = f.read()
                    st.success("✅ Hotel options!")

            except Exception as e:
                error_details = traceback.format_exc()
                st.error(f'❌ An error occurred: {str(e)}')
                st.code(error_details)  # Show stack trace for debugging
                st.session_state.planning_started = False
                return

    # Display Results After Planning
    if st.session_state.planning_started and st.session_state.itinerary:
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Itinerary", "🌤️ Weather", "✈️ Flights", "🏨 Hotels"])

        with tab1:
            st.subheader("📅 Your Customized Itinerary")
            st.markdown(st.session_state.itinerary)

        with tab2:
            st.subheader("🌤️ Weather Forecast")
            st.markdown(st.session_state.weather)

        with tab3:
            st.subheader("✈️ Best Flight Options")
            st.markdown(st.session_state.flights)

        with tab4:
            st.subheader("🏨 Recommended Hotels")
            st.markdown(st.session_state.hotels)

if __name__ == "__main__":
    main()