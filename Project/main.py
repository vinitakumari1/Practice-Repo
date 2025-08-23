import os
from fastapi import FastAPI
from api.weather_router import router as weather_router
from db.sql_db import Base, engine
from db_models.sql_model import WeatherForecast

Base.metadata.create_all(bind=engine)

API_KEY = os.getenv("WEATHER_API_KEY") 


app = FastAPI (title = "Weather Forecast Management")
app.include_router (weather_router)






