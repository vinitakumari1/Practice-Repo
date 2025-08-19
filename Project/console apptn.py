import requests



def get_weather_report(city,API_KEY):
    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"\n Weather Forecast for {city}\n")
            # show next 24 hours (8 entries, 3-hour interval)
            for forecast in data["list"][:8]:
                time = forecast["dt_txt"]
                temp = forecast["main"]["temp"]
                desc = forecast["weather"][0]["description"]
                print(f"{time} | Temp: {temp}°C | {desc}")
        else:
            print(f"\n Could not fetch weather for {city}")


if __name__ == "__main__":
   cities = ["London", "Paris", "New York", "Mumbai", "Tokyo"]
   for city in cities:
        get_weather_report(city=city,API_KEY="3747e640b1b9256cc2e4b8869262d3a3")