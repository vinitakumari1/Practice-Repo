from fastapi import FastAPI, Query
from app.service import index_resumes_service, ask_question_service
from app.model import QueryModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Resume QnA API"}

@app.post("/index")
def index_resumes():
    return index_resumes_service()

@app.post("/ask")
def ask_question(query: QueryModel):
    return ask_question_service(query.query)
