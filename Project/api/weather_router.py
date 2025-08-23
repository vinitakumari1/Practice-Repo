from fastapi import APIRouter, FastAPI, HTTPException,Depends
from api.models import CitiesRequest, SaveRequest
from api.services import fetch_weather, load_reports, save_reports

from db.sql_db import SessionLocal
from db_models.sql_model import WeatherForecast
from db.mongo_db import weather_collection
import datetime
import time
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def save_weather(city: str, db: Session = Depends(get_db)):
    # Fetch from API
    from api.services import fetch_weather
    data = fetch_weather(city)          # full dict
    forecasts = data["forecasts"]       # extract the list

    results = []
    for f in forecasts:
        time = datetime.datetime.strptime(f["time"], "%Y-%m-%d %H:%M:%S")
        temp = f["temperature"]         # correct key
        desc = f["description"]

        # ✅ Save to SQL
        sql_entry = WeatherForecast(
            city=city, time=time, temperature=temp, description=desc
        )
        db.add(sql_entry)

        # ✅ Save to Mongo
        mongo_doc = {
            "city": city,
            "time": time,
            "temperature": temp,
            "description": desc
        }
        weather_collection.insert_one(mongo_doc)

        results.append(mongo_doc)

    db.commit()
    return {"message": f"Saved 1 day forecast for {city}", "records": len(results)}


@router.get("/benchmark/{city}")
def benchmark(city: str, db: Session = Depends(get_db)):
    # SQL Query Benchmark
    start = time.time()
    sql_data = db.query(WeatherForecast).filter(WeatherForecast.city == city).all()
    sql_time = time.time() - start

    # MongoDB Query Benchmark
    start = time.time()
    mongo_data = list(weather_collection.find({"city": city}))
    mongo_time = time.time() - start

    return {
        "sql_time": f"{sql_time:.6f} sec",
        "mongo_time": f"{mongo_time:.6f} sec",
        "sql_records": len(sql_data),
        "mongo_records": len(mongo_data)
    }
