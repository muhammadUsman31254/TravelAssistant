# ✈️ AI Travel Assistant

Welcome to the **AI Travel Assistant**, powered by [crewAI](https://crewai.com)!  

![AI Travel Assistant](https://github.com/muhammadUsman31254/TravelAssistant/blob/main/Capture.PNG)

This intelligent application helps users plan their trips with ease by utilizing a collaborative, multi-agent AI system. It provides detailed **itineraries**, **weather forecasts**, **flight options**, and **hotel recommendations**—all automated and efficient.

## 🚀 Features

- 🗺️ Tailored trip itineraries
- 🌤️ Accurate destination weather forecasts
- ✈️ Optimal flight suggestions
- 🏨 Curated hotel recommendations

## 📦 Installation

### Requirements
- Python `>=3.10, <3.13`
- [UV](https://docs.astral.sh/uv/) for package management

### Setup Steps
1. **Install `uv`** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Install dependencies**:
   Navigate to your project directory:
   ```bash
   crewai install
   ```

## 🔧 Configuration

**Add your API_KEYS into the `.env` file**
- GROQ_API_KEY=your_key_here
- OPENWEATHER_API_KEY=your_key_here
- FLIGHT_API_KEY=your_key_here
- FLIGHT_API_SECRET=your_key_here
  
### Customize Configurations
- Agents: src/travel_assistant/config/agents.yaml
- Tasks: src/travel_assistant/config/tasks.yaml

### Modify Logic (Optional)
- Core Logic: src/travel_assistant/crew.py
- Custom Inputs: src/travel_assistant/main.py

## ▶️ Running the Project

From the root directory, launch the assistant:
```bash
$ crewai run
```

This command initializes your AI crew, assigns them tasks, and generates output files in the output/ directory:
- itinerary.md
- weather.md
- flights.md
- hotels.md

## 🗂️ Project Structure

```
travel_assistant/
├── src/
│   ├── travel_assistant/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── crew.py
│   │   ├── chat_assistant.py
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   ├── tasks.yaml
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── weather_tool.py
│   │   │   ├── flight_tool.py
│   │   │   ├── hotel_tool.py
├── output/
│   ├── itinerary.md
│   ├── weather.md
│   ├── flights.md
│   ├── hotels.md
├── .env
├── requirements.txt
```

## 🧠 Understanding Your Crew

The AI Travel Assistant is powered by specialized agents, each contributing their unique skillset to the trip planning process.

### 👥 Agents

| Agent | Role |
|-------|------|
| Travel Researcher | Discovers top attractions and activities at the destination |
| Itinerary Planner | Builds a day-by-day plan for the trip |
| Weather Forecaster | Provides weather data for the selected dates and location |
| Flight Finder | Finds optimal flights based on user inputs |
| Hotel Finder | Recommends hotels based on budget and preferences |

Agents and their tasks are defined in the `config/agents.yaml` and `config/tasks.yaml` config files, and orchestrated via the `crew.py` file.

## 📚 Support

For support, questions, or feedback regarding the TravelAssistant Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)

Let's build something amazing together with the power of crewAI.
