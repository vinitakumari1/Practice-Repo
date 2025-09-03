# Import necessary libraries
import json
import os
from fastapi import HTTPException   # to raise API errors
import requests                     # to make HTTP requests to OpenWeather API

# File where weather reports will be saved locally
SAVE_FILE = "weather_reports.json"  

# API key for OpenWeather (read from environment variable for security)
API_KEY = os.getenv("WEATHER_API_KEY")


def fetch_weather(city: str):
    """
    Fetch 1-day weather forecast for a given city from OpenWeather API.
    - Uses 5-day/3-hour forecast endpoint
    - Extracts only next 8 entries (24 hrs, 3hr gap each)
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract 24-hour forecast (next 8 intervals)
        forecast_data = [
            {
                "time": f["dt_txt"],                        # timestamp
                "temperature": f["main"]["temp"],           # temperature in Celsius
                "description": f["weather"][0]["description"]  # weather condition
            }
            for f in data["list"][:8]  # limit to 8 entries (~24 hours)
        ]

        # Return response in structured format
        return {
            "message": f"Fetched 1 day forecast for {city}",
            "forecasts": forecast_data
        }
    else:
        # If city not found or API error, raise 404
        raise HTTPException(status_code=404, detail=f"Could not fetch weather for {city}")


def load_reports():
    """
    Load saved weather reports from local JSON file.
    Returns empty dict if file does not exist.
    """
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)   # return existing reports as dict
    return {}  # return empty if no file found


def save_reports(data):
    """
    Save weather reports to local JSON file.
    - Overwrites previous content with updated data
    """
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)   # pretty-print JSON
