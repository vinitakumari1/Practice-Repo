import os
import faiss
import numpy as np


from openai import OpenAI
from pymongo import MongoClient
from uuid import uuid4


PDF_FOLDER = "resumes"
FAISS_INDEX_FILE = "resume_index.faiss"
INDEX_DATA_FILE="resume_chunks.npy"

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
DB_NAME = "resume_manager"
COLLECTION_NAME = "resume"

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
TEXT_EMBEDDINGS_MODEL="text-embedding-ada-002"

 #**********************intializeation*********
openai_client=OpenAI(api_key= OPENAI_API_KEY)
mongo_client=MongoClient(MONGO_URI)
db=mongo_client[DB_NAME]
resume_collection=db[COLLECTION_NAME]

#Connect to OpenAI and MongoDB
embedding_dim=1536
index=faiss.IndexFlatL2(embedding_dim)