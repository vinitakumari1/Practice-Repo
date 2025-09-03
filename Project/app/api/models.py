# Import Pydantic BaseModel for request validation
from pydantic import BaseModel


class CitiesRequest(BaseModel):
    """
    Request model for multiple city weather queries.
    - Expects a list of city names.
    
    Example:
    {
        "cities": ["London", "Paris", "Tokyo"]
    }
    """
    cities: list[str]


class SaveRequest(BaseModel):
    """
    Request model for saving a single city's weather report.
    - Expects only one city name.
    
    Example:
    {
        "city": "Berlin"
    }
    """
    city: str
