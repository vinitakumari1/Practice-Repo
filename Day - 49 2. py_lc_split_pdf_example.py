#write a program which will read the data from the pdf file
#Convert into the small chunks and summarize it



from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader
import os

#Step 1 : Load PDF file
pdf_path = "sample.pdf"
loader = PyPDFLoader(pdf_path)
pages=loader.load()


pdf_text = "\n".join([page.page_content for page in pages])
print(pdf_text)


# Step 2 : Split into chunks

RecursiveCharacterTextSplitter(
     chunk_size=10,
     chunk_overlap=5
)
chunks = RecursiveCharacterTextSplitter.split_text(pdf_text)
print(f"Total Chunks are : {len(chunks)}")

#Step 3 : Init LLM and steup prompt chain
llm=ChatOpenAI(model="gpt-4",temperature = 0.3)
prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize this chunk: \n {text}"
)

chain = LLMChain(llm=llm,prompt=prompt)


for i,chunk in enumerate(chunks):
    chunk_summary = chain.run({"text": chunk})
    print(f"\n--- Chunk {i+1} : {chunk} \nSummary ---\n {chunk_summary}")