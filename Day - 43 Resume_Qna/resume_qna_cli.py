import os
import faiss
import numpy as np
import fitz

from openai import OpenAI
from pymongo import MongoClient

#****************************configuration************

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

embedding_dim=1536
index=faiss.IndexFlatL2(embedding_dim)
index_data=[]

#*******************************
def ask_gpt4(query,context):
   context_block = "\n".join(context)
   messages = [
         {"role": "system", "content":"You are an helpful assistant that answers the questions based on the resume context"},
         {"role": "user", "content" : f"Context : \n {context_block} \n Question : {query}"}

   ]

   response= openai_client.chat.completions.create(
         model = "gpt-4",
         messages=messages,
         temperature=0.2
   )
   return response.choices[0].message.content.strip()

def load_index():
   if os.path.exists(FAISS_INDEX_FILE):
      global index,index_data
      index=faiss.read_index(FAISS_INDEX_FILE)
   if os.path.exists(INDEX_DATA_FILE):
      index_data=np.load(INDEX_DATA_FILE,allow_pickle=True).tolist()

def load_pdf_text(pdf_path):
   pdf_document = fitz.open(pdf_path)
   return "\n".join([ page.get_text() for page in pdf_document])
   
def chunk_text(text,chunk_size=2000):
    words=text.split()
    return[" ".join(words[i:i+chunk_size]) for i in range(0,len(words),chunk_size)]

def get_openai_embeddings_for_chunks(chunk_text):
      response= openai_client.embeddings.create(
         model= TEXT_EMBEDDINGS_MODEL,
         input= chunk_text
      )
      return response.data[0].embedding

def save_index():
   faiss.write_index(index,FAISS_INDEX_FILE)
   np.save(INDEX_DATA_FILE,index_data) #mapping resume with chunk


#***************************



def index_resumes():
   global index_data
   for filename in os.listdir(PDF_FOLDER):
      if filename.endswith(".pdf"):
         if resume_collection.find_one({"_id":filename}):
            print(f"Skipping : {filename} - already indexed")
            continue
         text=load_pdf_text(os.path.join(PDF_FOLDER,filename))
         chunks=chunk_text(text)
         for chunk in chunks:
            embedding= get_openai_embeddings_for_chunks(chunk)
            index.add(np.array([embedding],dtype="float32"))
            index_data.append({"_id": filename,"chunk":chunk})
            resume_collection.insert_one({"_id": filename,"text":chunk})
         print(f"Indexed the resume {filename}")

   save_index()

def query_resume(query):
   if index.ntotal==0 or len(index_data)==0:
      print("No resumes are indexed.Pleae use option 1.")
      return
   query_vector = get_openai_embeddings_for_chunks(query)
   X , I = index.search(np.array([query_vector],dtype="float32"),3) #Extract chunks matching query
  
   context= []
   for i in I[0]:
      if i < len(index_data):
         context.append(index_data[i]["chunk"])
   
   answer= ask_gpt4(query,context)
   print (answer)

def main():
   load_index()
   print(index_data)
   while True:
      print ("\n GPT4 Based resume Qna")
      print("1. Process the Resumes in Resume Folder")
      print("2. Ask Questions")
      print("3. Exit")
      Choice = input("Select an option : ")

      if Choice == "1":
         index_resumes()

      elif Choice =="2":
         query = input("Ask your question : ")
         query_resume(query)
      elif Choice =="3":
         print("Goodbye ! See you again...")
         break
      else:
         print("Invalid User Input.Please try again...")

if __name__=="__main__":
   main()

