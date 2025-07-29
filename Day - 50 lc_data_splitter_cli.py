#Write a CLI application which will ask the user to process the document on local or on web
# 1. Text document - .txt
# 2. Should be able to process the pdf doc
# 3. Word document - .docx
# 4. Markdown file - .md
# 5. HTML File - .html
# 6. JSON File - JSON
# 7. Web page - HTML

import os
import requests
import sys

from bs4 import BeautifulSoup

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    HTMLHeaderTextSplitter,
    TokenTextSplitter
)

from langchain_community.document_loaders import (
      TextLoader,
      PyPDFLoader,
      UnstructuredHTMLLoader,
      UnstructuredMarkdownLoader,
      UnstructuredWordDocumentLoader
)

from langchain.schema import Document


def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower() #(ameet.json = [ameet,json])
    
    if ext==".txt": #Load the files with .txt extension
        loader = TextLoader(file_path)
    elif ext == ".pdf":
        #Load the PDF using PyPDFLoader
        loader= PyPDFLoader(file_path)
    elif ext==".docx":
        loader= UnstructuredWordDocumentLoader(file_path)
    elif ext==".html":
        loader = UnstructuredHTMLLoader(file_path)
    elif ext == ".json":
        with open(file_path,"r",encoding="utf-8") as f:
            from langchain.schema import Document
            loader= [Document(page_content=f.read())]
            return loader 
    else:
        print("Unsupported file type.")
        sys.exit(1)
    return loader.load()
    
    
def load_url(url):
   response=requests.get(url=url)
   soup= BeautifulSoup(response.text,"html.parser")
   content = soup.get_text(separator="\n",)
   from langchain.schema import Document
   return [ Document(page_content= content)]



def menu():
    while True:
        print("---------Langchain Document Summarizer--------------")
        print("Choose a input type")
        print("1. Summarize the local file")
        print("2. Summarize the Web URL")
        choice = input("Pls enter a option")
        if choice =="1":
            file_Path=input("Enter the full path of the file:").strip()
            doc_content=load_file(file_Path)
            
        if choice =="2":
            url = input("Enter Web URL to crawl and summarize:")
            load_url(url)
        else:
            print("Invalid choice.Pls enter correct one")




if __name__ =="__main__":
    menu()