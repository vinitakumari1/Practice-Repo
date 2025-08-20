import requests
import os
import json

API_KEY = os.getenv("WEATHER_API_KEY")  # make sure this is set
OUTPUT_FILE = "weather_report.json"

def get_weather_report(city, api_key):
    """Fetch 1-day / 3-hour weather forecast for one city"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecasts = []
        for forecast in data["list"][:40]:  # next 24 hours
            time = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            desc = forecast["weather"][0]["description"]
            forecasts.append({
                "time": time,
                "temperature": temp,
                "description": desc
            })
        return { "city": city, "forecasts": forecasts }
    else:
        print(f"Could not fetch weather for {city}")
        return None

def save_to_json(data, filename):
    """Save collected weather data to JSON file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    cities = ["London", "Paris", "New York", "Mumbai", "Tokyo"]
    all_weather = []

    for city in cities: #fetches 1 day forecast for 5 cities and 1 day
        report = get_weather_report(city, API_KEY)
        if report:
            all_weather.append(report)

    # Save once at the end
    save_to_json(all_weather, OUTPUT_FILE)
    print(f"Weather reports saved to {OUTPUT_FILE}")
