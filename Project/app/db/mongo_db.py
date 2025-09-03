# Import MongoDB client
from pymongo import MongoClient
import os

# Read MongoDB URI from environment variable (fallback to default URI if not set)
MONGO_URL = os.getenv(
    "MONGO_URI", 
    "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
)

# Initialize MongoDB client
client = MongoClient(MONGO_URL)

# Select database and collection
mongo_db = client["weather_db"]                  # Database name: weather_db
weather_collection = mongo_db["weather_forecast"]  # Collection name: weather_forecast


# Create indexes for faster queries
weather_collection.create_index([("city", 1)])  
# ✅ Single-field index → makes queries like {"city": "London"} fast

# Compound index on (city + time)
# ✅ Useful for queries that filter by both city and timestamp
weather_collection.create_index([("city", 1), ("time", 1)])
