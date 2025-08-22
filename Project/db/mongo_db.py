from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URI", "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
client = MongoClient(MONGO_URL)

mongo_db = client["weather_db"]
weather_collection = mongo_db["weather_forecast"]
