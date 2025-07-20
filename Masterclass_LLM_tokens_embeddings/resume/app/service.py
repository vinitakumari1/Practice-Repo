import os
import numpy as np
import faiss
from uuid import uuid4
import fitz

from settings import FAISS_INDEX_FILE, INDEX_DATA_FILE, PDF_FOLDER, TEXT_EMBEDDINGS_MODEL, openai_client, resume_collection

index_data = []
index = faiss.IndexFlatL2(1536)

def ask_gpt4(query, context):
    context_block = "\n".join(context)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers the questions based on the resume context."},
        {"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {query}"}
    ]
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def load_index():
    global index, index_data
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
    if os.path.exists(INDEX_DATA_FILE):
        index_data = np.load(INDEX_DATA_FILE, allow_pickle=True).tolist()

def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in pdf_document])

def chunk_text(text, chunk_size=100):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def get_openai_embeddings_for_chunks(chunk_text):
    response = openai_client.embeddings.create(
        model=TEXT_EMBEDDINGS_MODEL,
        input=chunk_text
    )
    return response.data[0].embedding

def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    np.save(INDEX_DATA_FILE, index_data)

def index_resumes_service():
    global index_data
    load_index()
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            if resume_collection.find_one({"file": filename}):
                continue
            text = load_pdf_text(os.path.join(PDF_FOLDER, filename))
            chunks = chunk_text(text)
            for chunk in chunks:
                embedding = get_openai_embeddings_for_chunks(chunk)
                index.add(np.array([embedding], dtype="float32"))
                index_data.append({"_id": filename, "chunk": chunk})
                resume_collection.insert_one({"_id": str(uuid4()), "file": filename, "text": chunk})
    save_index()
    return {"status": "Resumes indexed successfully."}

def ask_question_service(query):
    load_index()
    if index.ntotal == 0 or len(index_data) == 0:
        return {"error": "No resumes indexed. Please index resumes first."}
    query_vector = get_openai_embeddings_for_chunks(query)
    D, I = index.search(np.array([query_vector], dtype="float32"), 3)
    context = []
    for i in I[0]:
        idx = int(i)  # Ensures it's a Python int
        if idx < len(index_data):
            context.append(index_data[idx]["chunk"])
    answer = ask_gpt4(query, context)
    return {"answer": answer}

