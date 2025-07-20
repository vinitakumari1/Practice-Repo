# 🧠 Masterclass: Building a Full-Stack "Chat with PDF" LLM App

Welcome to an end-to-end guide on building a **Chat with PDF** application using GPT-4, vector search (FAISS), embeddings, MongoDB, and FastAPI. This guide is perfect for developers looking to master real-world LLM app deployment.

---

## 📚 Table of Contents

1. [Query GPT-4 with context](#query-gpt-4-with-context)  
2. [Load index and data](#load-index-and-data)  
3. [Extract text from PDF](#extract-text-from-pdf)  
4. [Chunk text into pieces](#chunk-text-into-pieces)  
5. [Get OpenAI Embeddings](#get-openai-embeddings)  
6. [Save index to disk](#save-index-to-disk)  
7. [Index all resumes](#index-all-resumes)  
8. [Search and query](#search-and-query)  
9. [CLI entry point](#cli-entry-point)  
10. [FastAPI Endpoint (Optional Add-on)](#fastapi-endpoint)


---

## 1. Intro to LLM-Powered PDF Chat

The goal is simple: allow users to upload a PDF and chat with it.

**Core Workflow:**
1. User uploads a PDF.
2. Text is extracted and chunked.
3. Embeddings are generated and stored.
4. User asks a question.
5. System searches for relevant chunks.
6. GPT-4 formulates an answer using context.



---

## 2. Understanding Tokens and Text Chunking

### What Are Tokens?
Tokens are the building blocks of language models. For GPT models:
- A token may be as short as one character or as long as one word.

### Why Tokenization Matters
LLMs have a **token limit** per request. For GPT-4:
- Up to 8k or 32k tokens per prompt, depending on the model version.

### Example: Tokenization in Python
```python
from transformers import GPT2Tokenizer

text = "This is a sentence about PDF parsing."
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokens = tokenizer.tokenize(text)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print("Tokens:", tokens)
print("Token IDs:", token_ids)
```
**Output:**
```
Tokens: ['This', 'Ġis', 'Ġa', 'Ġsentence', 'Ġabout', 'ĠPDF', 'Ġparsing', '.']
Token IDs: [1212, 318, 257, 6827, 1112, 10272, 26136, 13]
```

---

## 3. Embeddings for Semantic Search

### What Are Embeddings?
Embeddings convert text into numerical vectors that capture meaning.

### Example: OpenAI Embeddings
```python
import openai
openai.api_key = "your-api-key"

response = openai.embeddings.create(
  model="text-embedding-3-small",
  input="What is the main argument of this PDF?"
)

embedding = response['data'][0]['embedding']
print("Embedding Vector (first 5 values):", embedding[:5])
```
**Output (truncated):**
```
Embedding Vector (first 5 values): [0.0123, -0.045, 0.0781, -0.0009, 0.0341]
```

---

## 4. PDF Text Extraction

### Using PyMuPDF
```python
import fitz  # PyMuPDF

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

text = extract_text("sample.pdf")
print(text[:500])
```
**Output (truncated):**
```
Introduction to AI
Artificial Intelligence (AI) is revolutionizing the way we interact with technology. In this document, we explore...
```


---

## 5. Creating Chunks for Indexing

### Chunking Strategy
```python
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

chunks = chunk_text(text)
print("Number of chunks:", len(chunks))
print("First chunk preview:\n", chunks[0][:300])
```
**Output (truncated):**
```
Number of chunks: 24
First chunk preview:
 Introduction to AI Artificial Intelligence (AI) is revolutionizing the way we interact with technology. In this document...
```

---

## 6. Storing and Querying with FAISS

### Vector Indexing

# faiss is a library developed by Facebook AI for efficient similarity search on large-scale vector datasets.
# 1536 - It is the dimension of each vector stored in the index.

```python
import faiss
import numpy as np

index = faiss.IndexFlatL2(1536) 

IndexFlatL2 is a type of index that performs brute-force search using L2 (Euclidean) distance.
vectors = np.array([chunk_vector1, chunk_vector2], dtype='float32')
index.add(vectors)
print("Total vectors indexed:", index.ntotal)
```
**Output:**
```
Total vectors indexed: 2
```

### Vector Search
```python
query_vector = np.array([your_query_vector], dtype='float32')
D, I = index.search(query_vector, k=1)
print("Top match index:", I[0][0])
```
**Output:**
```
Top match index: 0
```

---

## 7. Saving Metadata in MongoDB

### Resume Info, Source, Titles
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['chatpdf_db']
collection = db['chunks']

collection.insert_one({
    "chunk": "Introduction to AI ...",
    "embedding_id": 0,
    "source": "page 1",
    "doc_id": "sample_doc_01"
})
print("Chunk metadata inserted.")
```
**Output:**
```
Chunk metadata inserted.
```

---

## 8. FastAPI Backend for the App

### Endpoint for Query
```python
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    return {"answer": "To be implemented"}
```
**Output when running `uvicorn main:app --reload`:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 9. Handling Prompts with GPT-4

### Prompt Engineering
```python
context = "\n".join(top_chunks)
question = query["question"]

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
)

answer = response['choices'][0]['message']['content']
print(answer)
```
**Output (simulated):**
```
The main argument of this PDF is that Artificial Intelligence is transforming traditional industries by automating complex decision-making processes.
```

---
## 10-End-to end example:

# 🧠 LLM Resume QA Application - Full Code Reference

Below is the complete Python code for an LLM-powered resume Q&A application. It integrates FAISS for vector search, OpenAI for embeddings, PyMuPDF for PDF parsing, MongoDB for metadata storage, and a simple CLI for interaction.

---

## 📦 `resume_qa_app.py`

```python
import os
from uuid import uuid4

import faiss
import fitz
import numpy as np
from settings import FAISS_INDEX_FILE, INDEX_DATA_FILE, PDF_FOLDER, TEXT_EMBEDDINGS_MODEL, openai_client, resume_collection

index_data = []

# Query GPT-4 with context

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

# Load index and data

def load_index():
    global index, index_data
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
    if os.path.exists(INDEX_DATA_FILE):
        index_data = np.load(INDEX_DATA_FILE, allow_pickle=True).tolist()

# Extract text from PDF

def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    print(f"The total number of pages is {len(pdf_document)}")
    return "\n".join([page.get_text() for page in pdf_document])

# Chunk text into pieces

def chunk_text(text, chunk_size=100):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Get OpenAI Embeddings

def get_openai_embeddings_for_chunks(chunk_text):
    response = openai_client.embeddings.create(
        model=TEXT_EMBEDDINGS_MODEL,
        input=chunk_text
    )
    return response.data[0].embedding

# Save index to disk

def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    np.save(INDEX_DATA_FILE, index_data)

# Index all resumes

def index_resumes():
    global index_data
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            if resume_collection.find_one({"file": filename}):
                print(f"Skipping: {filename} - already indexed")
                continue

            text = load_pdf_text(os.path.join(PDF_FOLDER, filename))
            chunks = chunk_text(text)

            for chunk in chunks:
                embedding = get_openai_embeddings_for_chunks(chunk)
                index.add(np.array([embedding], dtype="float32"))
                index_data.append({"_id": filename, "chunk": chunk})

                resume_collection.insert_one({"_id": str(uuid4()), "file": filename, "text": chunk})

            print(f"Indexed the resume {filename}")

    save_index()

# Search and query

def query_resume(query):
    if index.ntotal == 0 or len(index_data) == 0:
        print("No resumes are indexed. Please use option 1.")
        return

    query_vector = get_openai_embeddings_for_chunks(query)
    I = index.search(np.array([query_vector], dtype="float32"), 3)

    context = []
    for i in I[0]:
        i = int(i)
        if i < len(index_data):
            context.append(index_data[i]["chunk"])

    answer = ask_gpt4(query, context)
    print(answer)

# CLI entry point

def main():
    load_index()
    while True:
        print("\n🔍 GPT-4 Based Resume Q&A")
        print("1. Process the Resumes in Resume Folder")
        print("2. Ask Questions")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            index_resumes()
        elif choice == "2":
            query = input("Ask your question: ")
            query_resume(query)
        elif choice == "3":
            print("Goodbye! See you again...")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

# fastapi_app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
load_index()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask(question: Question):
    answer = query_resume(question.query)
    return {"answer": answer}
```

---

This code supports:

- **PDF extraction with PyMuPDF**
- **Text chunking for long content**
- **Embedding generation via OpenAI**
- **Vector storage with FAISS**
- **Metadata storage in MongoDB**
- **Q&A using GPT-4 over top-matching vector chunks**


## 11. Some Brain-Storming Questions :

🔹 Tokenization & Chunking
1. What is a token in the context of language models, and why is tokenization critical?

2. Explain why overlapping chunks are often used when splitting long texts for language models.

3. How would you determine the optimal chunk size and overlap for text preprocessing in a production system?

🔹 Embeddings & Semantic Representation
1. What are text embeddings, and how do they support semantic similarity tasks?

2. What are some common use cases where vector embeddings are more effective than keyword search?

3. What are the differences between sentence embeddings and word embeddings? When would you use each?

🔹 Vector Indexing & Search (FAISS)
1. What is FAISS and how does it improve performance for similarity search in high-dimensional space?

2. Explain L2 distance vs cosine similarity in vector search. Which would you choose and why?

3. What considerations should be taken when selecting the dimensionality for your vector index?

4. What are some alternatives to FAISS for similarity search, and when might they be preferable?

🔹 NoSQL Data Management (MongoDB)
5. Why might MongoDB be chosen to store metadata alongside embeddings or vector indices?

6. What are the pros and cons of using a document-based database like MongoDB for LLM applications?

7. How would you structure your MongoDB collections to support multi-user access and scalability?

🔹 FastAPI & Backend Design
8. What are the key benefits of using FastAPI for building AI-powered microservices?

9. How would you design an endpoint to accept user queries, process embeddings, and return model responses?

10. What are Pydantic models, and how do they help validate and document APIs in FastAPI?

🔹 Prompt Engineering & Model Interaction
11. What is prompt engineering, and why is it essential when working with large language models?

12. How would you design a system to dynamically build prompts from retrieved content before sending them to an LLM?

🔹 Deployment & Security
13. What are some best practices to deploy a FastAPI app in production securely and scalably?

14. How would you implement rate-limiting and API authentication in a FastAPI-based application?


