import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import API routes and database setup
from app.api.weather_router import router as weather_router
from app.db.sql_db import Base, engine, init_db

# Read Weather API key from environment variables (for external API calls)
API_KEY = os.getenv("WEATHER_API_KEY")


# --- Lifespan handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context for FastAPI app.
    Runs startup and shutdown tasks for the application.
    """
    # ✅ Startup: Initialize SQL database (create tables, seed data if needed)
    Base.metadata.create_all(bind=engine)
    init_db()
    
    yield   # Application runs while this is active
    
    # ✅ Shutdown: (Optional cleanup tasks if needed)
    # Example: close connections, clear caches, stop background workers


# Initialize FastAPI app with lifespan handler
app = FastAPI(
    title="Weather Forecast Management",   # API title (shown in Swagger UI)
    lifespan=lifespan
)

# Register weather routes
app.include_router(weather_router)
