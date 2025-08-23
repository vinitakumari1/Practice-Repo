from sqlalchemy import Column, Integer, String, Float, DateTime
from db.sql_db import Base

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False)   # length added
    time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)  # length added


