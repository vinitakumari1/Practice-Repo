
# Write an Program which will read the data from Website URL-https://www.virtualglobetechnology.com/testimonial 
# and convert into thee small chunks and summerize it. and save to the txt file
#Web URL - pip install requests 



from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os

from bs4 import BeautifulSoup
import requests


url = "https://www.virtualglobetechnology.com/testimonial"
output_file = "web_crawl_summary.txt"

# Step 1 : Load and read the URL
response = requests.get(url=url)
soup = BeautifulSoup(response.text,"html.parser")
original_text= soup.get_text(separator= "\n")

print(f"Original TEXT :{original_text}")
cleaned_text = "\n".join(line.strip() for line in original_text.splitlines() if line.strip())

print(f"Original TEXT :{cleaned_text}")

#step 2 : Split the text and get small chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50
)

chunks=splitter.split_text(cleaned_text)


#Step 3 : Init LLM and setup Prompt and chain
llm= ChatOpenAI(model="gpt-4",temperature=0.3)

prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize this chunk: \n {text}"
)

chain = LLMChain (llm=llm,prompt = prompt)


#summarize and save to file
with open (output_file,"w",encoding="utf-8") as f:
    for i,chunk in enumerate (chunks):
        summary_text = chain.run({"text":chunk})
        f.write(f"\n--- Chunk {i+1} ---\n")
        f.write(f"original :{chunk} \n")
        f.write(f"Summary: \n {summary_text} \n ")

print(f"Web URL Crawling is done for url {url}")
print(f"and summary is saved to {output_file}.")