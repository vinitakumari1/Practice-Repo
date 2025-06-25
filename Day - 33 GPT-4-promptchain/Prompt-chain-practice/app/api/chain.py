from pydantic import BaseModel

class TextInput(BaseModel):
    text: str
    language : str ="hi"



