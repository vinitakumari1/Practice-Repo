# Import necessary libraries
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from app.api.models import CitiesRequest, SaveRequest     # Pydantic models for request validation
from app.api.services import fetch_weather, load_reports, save_reports  # Business logic functions

from app.db.sql_db import SessionLocal       # SQLAlchemy session factory
from app.db_models.sql_model import WeatherForecast   # SQLAlchemy ORM model
from app.db.mongo_db import weather_collection        # MongoDB collection instance
import datetime
import time
from sqlalchemy.orm import Session

# Initialize router for modular routes
router = APIRouter()


# Dependency for SQLAlchemy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db     # provide session to route
    finally:
        db.close()   # always close session after request


# Root endpoint (Health check)
@router.get("/")
def root():
    return {"message": "Weather API is running"}


# Get weather data for a single city (calls external API/service)
@router.get("/weather/{city}")
def get_weather(city: str):
    return fetch_weather(city)


# Get weather data for multiple cities
@router.post("/weather/multiple")
def get_multiple_weather(request: CitiesRequest):
    results = []
    for city in request.cities:
        try:
            results.append(fetch_weather(city))   # fetch each city
        except HTTPException as e:
            # if error occurs, return city with error message
            results.append({"city": city, "error": str(e.detail)})
    return results


# Save weather report for one city (JSON file storage)
@router.post("/weather/save")
def save_weather(request: SaveRequest):
    data = fetch_weather(request.city)    # fetch weather data
    reports = load_reports()              # load existing reports
    reports[request.city] = data          # add/overwrite city report
    save_reports(reports)                 # save back to file
    return {"message": f"Weather for {request.city} saved successfully"}


# Get all saved reports (JSON file)
@router.get("/reports")
def get_reports():
    return load_reports()


# Delete a report for a given city
@router.delete("/reports/{city}")
def delete_report(city: str):
    reports = load_reports()
    if city in reports:
        del reports[city]                 # remove city report
        save_reports(reports)
        return {"message": f"Report for {city} deleted"}
    # if not found, raise 404
    raise HTTPException(status_code=404, detail=f"No report found for {city}")


# Save weather data for a city into both SQL and MongoDB
@router.post("/weather/save/{city}")
def save_weather(city: str, db: Session = Depends(get_db)):
    from app.api.services import fetch_weather
    data = fetch_weather(city)            # fetch full weather data
    forecasts = data["forecasts"]         # extract forecasts list

    results = []
    sql_entries = []   # SQLAlchemy ORM objects
    mongo_docs = []    # MongoDB documents

    # Loop over each forecast entry
    for f in forecasts:
        time = datetime.datetime.strptime(f["time"], "%Y-%m-%d %H:%M:%S")
        temp = f["temperature"]
        desc = f["description"]

        # ✅ Prepare SQL entries
        sql_entries.append(
            WeatherForecast(city=city, time=time, temperature=temp, description=desc)
        )

        # ✅ Prepare Mongo documents
        mongo_docs.append({
            "city": city,
            "time": time,
            "temperature": temp,
            "description": desc
        })

    # Bulk insert into SQL database
    db.add_all(sql_entries)
    db.commit()

    # Bulk insert into MongoDB
    if mongo_docs:
        weather_collection.insert_many(mongo_docs)

    return {
        "message": f"Saved 1 day forecast for {city}",
        "records": len(forecasts)
    }


# Benchmark query performance between SQL and MongoDB
@router.get("/benchmark/{city}")
def benchmark(city: str, db: Session = Depends(get_db)):
    # ✅ SQL Query Benchmark
    start = time.time()
    sql_data = db.query(WeatherForecast).filter(WeatherForecast.city == city).all()
    sql_time = time.time() - start

    # ✅ MongoDB Query Benchmark
    start = time.time()
    mongo_data = list(weather_collection.find({"city": city}))
    mongo_time = time.time() - start

    # Return both timings + record counts
    return {
        "sql_time": f"{sql_time:.6f} sec",
        "mongo_time": f"{mongo_time:.6f} sec",
        "sql_records": len(sql_data),
        "mongo_records": len(mongo_data)
    }
