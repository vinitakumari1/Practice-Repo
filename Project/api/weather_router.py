from fastapi import APIRouter, FastAPI, HTTPException,Depends
from api.models import CitiesRequest, SaveRequest
from api.services import fetch_weather, load_reports, save_reports


from db.mongo_db import weather_collection
import datetime
import time


router = APIRouter()




@router.get("/")
def root():
    return {"message": "✅ Weather API is running"}

@router.get("/weather/{city}")
def get_weather(city: str):
    return fetch_weather(city)

@router.post("/weather/multiple")
def get_multiple_weather(request: CitiesRequest):
    results = []
    for city in request.cities:
        try:
            results.append(fetch_weather(city))
        except HTTPException as e:
            results.append({"city": city, "error": str(e.detail)})
    return results

@router.post("/weather/save")
def save_weather(request: SaveRequest):
    data = fetch_weather(request.city)
    reports = load_reports()
    reports[request.city] = data
    save_reports(reports)
    return {"message": f"Weather for {request.city} saved successfully"}

@router.get("/reports")
def get_reports():
    return load_reports()

@router.delete("/reports/{city}")
def delete_report(city: str):
    reports = load_reports()
    if city in reports:
        del reports[city]
        save_reports(reports)
        return {"message": f"Report for {city} deleted"}
    raise HTTPException(status_code=404, detail=f"No report found for {city}")




@router.post("/weather/save/{city}")
def save_weather(city: str):
    # Fetch from API
    from api.services import fetch_weather
    data = fetch_weather(city)          # full dict
    forecasts = data["forecasts"]       # extract the list

    results = []
    for f in forecasts:
        time = datetime.datetime.strptime(f["time"], "%Y-%m-%d %H:%M:%S")
        temp = f["temperature"]         # correct key
        desc = f["description"]

     

        # ✅ Save to Mongo
        mongo_doc = {
            "city": city,
            "time": time,
            "temperature": temp,
            "description": desc
        }
        weather_collection.insert_one(mongo_doc)

        results.append(mongo_doc)

    return {"message": f"Saved forecast for {city}", "records": len(results)}

