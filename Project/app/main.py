from fastapi import FastAPI
from api.weather_router import router as weather_router

app = FastAPI (title = "Weather forecast Management")
app.include_router (weather_router)