# Pydantic model
from pydantic import BaseModel
class Book(BaseModel):
    id: int
    bookname: str
    quantity: int
    author: str


class BookDeleteRequest(BaseModel):
    book_id:int


class GetBookbyIDRequest(BaseModel):
    book_id:int