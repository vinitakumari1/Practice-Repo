#write an program to take long text and chunk into smaller parts.
#send each chunk to GPT4 and ask to summarize it.


#pip install langchain langchain_openai openai tiktoken langchain_community --upgrade
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os



# Step 1 : Get the long text
long_text= """
LangChain is an open-source framework designed to simplify the development of 
applications that integrate with large language models (LLMs) like GPT. 
It provides a modular structure for building complex LLM-powered systems 
by offering components such as prompt templates, chains, memory, agents, 
and tools. LangChain supports various use cases, including question answering,
summarization, document retrieval, and chatbots, by allowing developers to easily 
connect LLMs with external data sources (like databases, APIs, or PDFs).
Its ability to combine LLMs with logic, memory, and external tools makes it 
especially powerful for creating intelligent and dynamic applications.
"""

#['LangChain is an open-source framework designed to',
#  'to simplify the development of \napplications that',
#  'that integrate with large language models (LLMs)', 
# '(LLMs) like GPT', 
# '. \nIt provides a modular structure for building',
#  'building complex LLM-powered systems \nby offering', 
# 'offering components such as prompt templates,',
#  'chains, memory, agents, \nand tools', 
# '. LangChain supports various use cases, including', 
# 'including question answering,\nsummarization,',
#  'document retrieval, and chatbots, by allowing',
#  'allowing developers to easily \nconnect LLMs with',
#  'LLMs with external data sources (like databases,', 'APIs, or PDFs)',
#  '.\nIts ability to combine LLMs with logic, memory,',
#  'memory, and external tools makes it \nespecially', 
# 'powerful for creating intelligent and dynamic', 
# 'dynamic applications', '.']


# Step 2 : Split the text and get the chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
     chunk_overlap= 10,
     separators= ["\n\n","."," ","","\n"]
)

chunks = splitter.split_text(long_text)

print(f"Total length {len(chunks)}")

#Step 3 : Send each chunk to GPT 4 for summarizing
llm=ChatOpenAI(model="gpt-4", temperature=0.3)

prompt = PromptTemplate(
     input_variables = ["text"],
     template = "Summarize this chunk :\n {text}"  #dont use f here
)
chain = LLMChain (llm=llm, prompt=prompt)

for i,chunk in enumerate(chunks):
    summary= chain.run({"text" : chunk})
    print(f"\n ---- Chunk {i+1} : {chunk} \n Summary is : {summary}")









