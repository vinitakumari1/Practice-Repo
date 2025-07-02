from app.core.Exceptions import (
    Book_already_exists_Exception,
      Book_not_Found_Exception
)

from app.core.logging import (
load_books,
 save_books,
 logger
)

from app.models.model import Book, BookDeleteRequest, GetBookbyIDRequest
from fastapi import APIRouter

router = APIRouter()

# ✅ Meaning of router = APIRouter()
# APIRouter is a class from FastAPI used to group related API endpoints.

# You create a router object with it, just like you create an app with FastAPI().

# Instead of registering routes directly on the app, you register them on the router.

# Later, you include the router into the main app using app.include_router(router).


# 📌 Benefits of Using APIRouter
# Benefit	Description
# 🔌 Modular	Keeps code organized by splitting routes across files
# ♻️ Reusable	You can reuse routers in multiple apps/microservices
# 🧱 Scalable	Easy to add routers for users, books, orders, etc.
# 🗂️ Tagged Docs	Each router can have its own section in Swagger UI

# # Utility functions
# def load_books():
#     if not os.path.exists('books.json'):
#         logger.warning("books.json not found.")
#         return []
#     with open('books.json', 'r') as f:
#         logger.info("Loaded books from JSON.")
#         return json.load(f)

# def save_books(data):
#     with open('books.json', 'w') as f:
#         json.dump(data, f, indent=4)
#         logger.info("Saved books to JSON.")

# Routes
@router.get("/health_check")
async def app_health_check():
    logger.info("App health check successful")
    return {"status": "App is running fine"}


@router.get("/get_all_books")
async def get_books():
     books=load_books()
     logger.info("All the books fetched from json")
     return list(books)




@router.post("/get_book_details")
async def find_book(data: Book):
    books = load_books()
    for book in books:
        if (
            book["id"] == data.id and
            book["bookname"] == data.bookname and
            book["author"] == data.author and
            book["quantity"] == data.quantity
        ):
            logger.info(f"Book found: {data.bookname}")
            return {"message": "Book found successfully"}
    raise Book_not_Found_Exception()

@router.post("/get_book_by_id")
async def get_book_by_id(data:GetBookbyIDRequest):
    books=load_books()
    for book in books:
        if book["id"] == data.book_id:
            logger.info(f"Searching for book with book id {data.book_id}")
            return {"message" : f"Book with book id {book["id"]} is found",
                    "book": book }
    logger.info(f"Book with {data.book_id} not found")
    raise Book_not_Found_Exception()

@router.post("/save_book")
async def save_book(data: Book):
    books = load_books()
    for book in books:
        if book["id"] == data.id:
            raise Book_already_exists_Exception()
    books.append(data.dict())
    save_books(books)
    logger.info(f"Book added: {data.bookname}")
    return {"message": "Book saved successfully"}

@router.get("/get_book_names")
async def get_book_names():
    books=load_books()
    
    return [(book["bookname"]) for book in books]
        
# @router.get("/get_book_names")
# async def get_book_names():
#     books = load_books()
#     # names = [book["bookname"] for book in books]
#     return ([book["bookname"] for book in books])




@router.post("/delete_book")
async def delete_book(data:BookDeleteRequest):
    books=load_books()
    new_books = [book for book in books if book["id"] != data.book_id]
    if len(new_books) == len(books):
        raise Book_not_Found_Exception()
    save_books(new_books)
    logger.info(f"Book with {data.book_id} is deleted")
    return {"message": "Book deleted successfully","books": new_books}







    