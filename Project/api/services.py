import json
import os
from fastapi import HTTPException
import requests

SAVE_FILE = "weather_reports.json"
API_KEY =os.getenv("WEATHER_API_KEY")



def fetch_weather(city: str):
    """Fetch 1-day weather forecast for a city from OpenWeather API"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast_data = [
            {
                "time": f["dt_txt"],
                "temperature": f["main"]["temp"],
                "description": f["weather"][0]["description"]
            }
            for f in data["list"][:8]  # next 24 hrs (3hr intervals → 8 slots)
        ]
        return{"message":f"Fetched 1 day forecast for {city}",  "forecasts": forecast_data}
        
    else:
        raise HTTPException(status_code=404, detail=f"Could not fetch weather for {city}")

def load_reports():
    """Load saved weather reports"""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_reports(data):
    """Save weather reports to file"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

