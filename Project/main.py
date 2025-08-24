import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.weather_router import router as weather_router
from app.db.sql_db import Base, engine, init_db
API_KEY = os.getenv("WEATHER_API_KEY")


# --- Lifespan handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB
    Base.metadata.create_all(bind=engine)
    init_db()
    yield
    # Shutdown: (optional cleanup if needed)


app = FastAPI(title="Weather Forecast Management", lifespan=lifespan)
app.include_router(weather_router)









