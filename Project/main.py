import os
from fastapi import FastAPI
from api.weather_router import router as weather_router



API_KEY = os.getenv("WEATHER_API_KEY")


app = FastAPI (title = "Weather Forecast Management")
app.include_router (weather_router)






