from pydantic import BaseModel




class CitiesRequest(BaseModel):
    cities: list[str]

class SaveRequest(BaseModel):
    city: str