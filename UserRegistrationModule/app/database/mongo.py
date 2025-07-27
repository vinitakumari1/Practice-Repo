from pymongo import MongoClient
import os



MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
DB_NAME = "usermanagement"
COLLECTION_NAME = "users"




#db and collection configuration
client = MongoClient(MONGO_URI) #connect to mongo cluster
database=client[DB_NAME] #get access to database
users=database[COLLECTION_NAME]