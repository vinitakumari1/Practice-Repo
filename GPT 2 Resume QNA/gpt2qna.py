import fitz
import logging
import os 
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model
from pymongo import MongoClient


MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
DB_NAME = "resume_manager"
COLLECTION_NAME = "resume"

mongo_client=MongoClient(MONGO_URI)
db=mongo_client[DB_NAME]
resume_collection=db[COLLECTION_NAME]

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

# Add Padding Tokens {Becuase this is not default in GPT2}
tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

PDF_FOLDER = r"C:\Agentic-AI Trainings\Day-26_LLM\Day - 43 Resume_Qna\Resumes"
JD_FOLDER= r"C:\Agentic-AI Trainings\Day-26_LLM\Day - 43 Resume_Qna\JD"


logging.basicConfig(
    filename='gpt2resumeqna.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.getLogger()

def load_pdf_text(pdf_path):
   pdf_document = fitz.open(pdf_path)
   return "\n".join([ page.get_text() for page in pdf_document])


def chunk_text(text,chunk_size=50):
    words=text.split()
    return[" ".join(words[i:i+chunk_size]) for i in range(0,len(words),chunk_size)]


def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = emb_model(
            input_ids=input_text_tokens["input_ids"],
            attention_mask=input_text_tokens["attention_mask"]
        )
    return embeddings.last_hidden_state.mean(dim=1)  # shape: [1, 768]

def index_resume():
   for filename in os.listdir(PDF_FOLDER):
      if filename.endswith(".pdf"):
         logging.info("Found the files to be indexed")
         text=load_pdf_text(os.path.join(PDF_FOLDER,filename))
         chunks=chunk_text(text)
         logging.info("Chunked the text")
         for chunk in chunks:
            embedding=get_mean_embedding(chunk)
            resume_collection.insert_one({"filename": filename, "chunk": chunk, "embedding" :embedding.squeeze().tolist()})
      logging.info("Indexed the file to MongoDB")
      print (f"Indexed the {filename} successfully")
              

def query_resume(prompt):
    combined_resume_text = ""

    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            resume_text = load_pdf_text(os.path.join(PDF_FOLDER, filename))
            combined_resume_text += resume_text + "\n"

    # Truncate to fit within model limits
    truncated_text = combined_resume_text[:1500]  # keep it short for GPT-2

    full_prompt = f"Here is a resume document:\n\n{truncated_text}\n\nTask: {prompt}\nSummary:"

    inputs = tokenizer(full_prompt, return_tensors="pt", padding=True, truncation=True)

    answers = gen_model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        do_sample=True,
        num_return_sequences=3,
        max_new_tokens=100,
        temperature=0.8,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )

    return [
        tokenizer.decode(ans, skip_special_tokens=True).replace(full_prompt, "").strip()
        for ans in answers
    ]


def similarity():
    for jd_file in os.listdir(JD_FOLDER):
        if not jd_file.endswith(".pdf"):
            continue

        jd_path = os.path.join(JD_FOLDER, jd_file)
        jd_text = load_pdf_text(jd_path)
        jd_mean_embeddings = get_mean_embedding(jd_text)

        print(f"\n Job Description: {jd_file}")
        
        for resume_file in os.listdir(PDF_FOLDER):
            if not resume_file.endswith(".pdf"):
                continue

            resume_path = os.path.join(PDF_FOLDER, resume_file)
            resume_text = load_pdf_text(resume_path)
            resume_mean_embeddings = get_mean_embedding(resume_text)

            score = F.cosine_similarity(resume_mean_embeddings, jd_mean_embeddings).item()
            print(f"Resume: {resume_file} | Similarity Score: {score:.4f}")


def main():
 while True:
   print("\n Please enter option : ")
   print("1. Index the resume.")
   print("2. Ask the query")
   print("3. Similarity score with the JD")
   print("4. Exit")
   
   choice= input("pls enter correct option: ")
   if choice == "1":
     index_resume()

   elif choice == "2":
    prompt = input("Please enter the query: ")
    answers = query_resume(prompt)
    print("\nGenerated Answers:")
    for i, ans in enumerate(answers, 1):
        print(f"{i}. {ans}")


   elif choice == "3":
     similarity()
   
   elif choice == "4":
     print("Goodbye ! Exiting.........")
     break
   
   else:
    print("pls enter correct option")
   


if __name__ == "__main__":
    main()


# def index_resume():
#     document = os.path.join(RESUME_FOLDER, "offer_letter.txt")  # update file name accordingly
#     if not os.path.exists(document):
#         print(f"File not found: {document}")
#         return

#     with open(document, "r", encoding='utf-8') as f:
#         words = f.read().split()
#     print("First 20 words from the resume:", words[:20])  # Just print a sample



# def main():
#     while True:
#         print("\nPlease enter option:")
#         print("1. Index the resume")
#         print("2. Ask a query")
#         print("3. Similarity score with the JD")
#         print("4. Exit")

#         try:
#             choice = int(input("Please enter your choice: "))
#         except ValueError:
#             print("Invalid input. Enter a number between 1-4.")
#             continue

#         if choice == 1:
#             index_resume()
#         elif choice == 2:
#             query_resume()
#         elif choice == 3:
#             print("Similarity scoring not implemented yet.")
#         elif choice == 4:
#             print("Exiting.")
#             break
#         else:
#             print("Please choose a valid option (1-4).")

# if __name__ == "__main__":
#     main()



