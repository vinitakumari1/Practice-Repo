# Import SQLAlchemy column types and Base class
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.sql_db import Base


class WeatherForecast(Base):
    """
    SQLAlchemy ORM model for storing weather forecast data in SQL database.
    Each row represents a single forecast entry (city, timestamp, temperature, description).
    """

    # Table name in the database
    __tablename__ = "weather_forecast"

    # Auto-incrementing primary key
    id = Column(Integer, primary_key=True, index=True)

    # City name (max length 100 characters, cannot be NULL)
    city = Column(String(100), nullable=False)

    # Forecast time (date + time, cannot be NULL)
    time = Column(DateTime, nullable=False)

    # Temperature (float value in Celsius, cannot be NULL)
    temperature = Column(Float, nullable=False)

    # Weather description (e.g., "clear sky", "light rain")
    description = Column(String(255), nullable=False)
