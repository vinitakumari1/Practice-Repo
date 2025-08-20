from fastapi import APIRouter, FastAPI, HTTPException
from api.models import CitiesRequest, SaveRequest
from api.services import fetch_weather, load_reports, save_reports



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
