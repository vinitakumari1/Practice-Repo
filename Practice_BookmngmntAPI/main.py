from fastapi import FastAPI
from app.services.APIRouter import router  # Import the router

app = FastAPI()

# Include the router from book_service
app.include_router(router, prefix="/api", tags=["Books Management System"])


# Meaning Explained:
# 1. from fastapi import FastAPI
# ➡️ This imports the FastAPI class to create a web API.

# 2. from app.services.APIRouter import router
# ➡️ You're importing the router object from a file named APIRouter.py, located inside:


# app/
# └── services/
#     └── APIRouter.py
# 📝 That router should be an instance of APIRouter, which holds all your route definitions (like /save_book, /get_all_books, etc.).

# 3. app = FastAPI()
# ➡️ Creates an instance of the FastAPI application — this is the main app that runs the server.

# 4. app.include_router(router, prefix="/api", tags=["Books Management System"])
# This registers the imported router with your main app.

# router: The APIRouter object that contains endpoints.

# prefix="/api": Adds /api in front of every route (e.g., /get_all_books becomes /api/get_all_books).

# tags=["Books Management System"]: Groups all routes in Swagger UI under the label "Books Management System".

# ✅ What This Enables:
# When you visit http://127.0.0.1:8000/docs, you will see all the API routes from your router grouped under:

# ▶️ Books Management System
# Each route will start with /api/....

# 🗺️ Visual Summary:
# text
# Copy
# Edit
# URL:                    Functionality:
# ----------------------  --------------------------------------
# /api/get_all_books      -> Returns all books
# /api/save_book          -> Adds a new book
# /api/delete_book        -> Deletes a book