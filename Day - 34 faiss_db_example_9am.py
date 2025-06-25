from openai import OpenAI # pip install openai
import numpy as np # Used to vector math and array conversation
import pickle # Save and Load Dictionary (label to Index) - Heatmap
import faiss # pip install faiss
import os


# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX = "text_index.faiss" # faiss database
LABEL_MAP_FILE = "text_label.pk1" # pickle
VECTOR_DIM = 1536 # - Embeddings - Mean, Full -> Mean -> 768 -d (GPT2) : GPT4 : 1536



# Init Open AI GPT4 - Client 
client = OpenAI (api_key = os.getenv("OPENAI_API_KEY")) # always read from Enviroments

# Create or use existing Index
if os.path.exists(FAISS_INDEX):
    index = faiss.read_index(FAISS_INDEX) # Use Existing Index
else:
    index = faiss.IndexFlatL2 (VECTOR_DIM) # Create Index

# Create or Init Pickle file 
if os.path.exists(LABEL_MAP_FILE):
    with open (LABEL_MAP_FILE, "rb") as f:
        label_map = pickle.load(f)
else:
    label_map = {} # {index, label}

def get_embeddings(text:str) -> list:
    # Model is text-embedding-3-small used to get embeddings for text
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding # Return final embeddings

def add_to_index():
    text  = input ("Enter text to add to faiss db (index): ") # text = How are you Manish
    label  = input ("Enter lable for text {text} : ") # label = Manish

    text_embeddings = get_embeddings(text) # Get the embeddings for text
    print (f"text_embeddings : {text_embeddings}")

    vector = np.array([text_embeddings]).astype("float32")
    print (f"vector : {vector}")  

    index_id = index.ntotal # Current size of total vectors
    print (f"index_id : {index_id}")  

    index.add(vector) # Add to Index (Faiss DB) -> Float 32 - Embedings -> Vector
    label_map[index_id] = label
    save_index()



def save_index(): # Save Index to local db {faiss db}
    faiss.write_index(index,FAISS_INDEX)
    with open (LABEL_MAP_FILE, "wb") as f:
        pickle.dump (label_map, f)

def list_labels():
    for idx, label in label_map.items():
        print (f"{idx} : {label}")

def compare_labels():
    first_label = input("Enter the name of first label")
    second_label = input("Enter the name of second label")
    for idx,label in label_map.items(): #iterate for evry row in collection
        if label == first_label:
            return 1
        if label == second_label:
            return 2


def main():
    add_to_index()
    # list_labels()
    compare_labels()




if __name__ == "__main__":
    main()