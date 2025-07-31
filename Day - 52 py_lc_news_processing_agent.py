"""
Autonomous news processing agent using langchain
- Downloads latest news articles
- rewords each article
- detects category
- suggests hashtags
- saves evrything to JSON for download

"""

#connect to news api
# download news
# reword news
# detect news category
# get the hashtags
# child safe
#save the news => publish => SQL server , MONGO ,SQS,AWS S3 Bucket

# Config/ Settings

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "30ddaecf408f424bbb54466657be12fb"
COUNTRY ="us"
ARTICLE_COUNT=2
OUTPUT_FILE = "processed_news.json"

# import langchain modules for agent creation
import requests
import json
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent,Tool
from langchain.memory import ConversationBufferMemory

# llm -setup create and init LLM

# create and init LLM
llm= ChatOpenAI(
    model="gpt-4",
    temperature = 0.3
)
 
processed_result =[]

#Tools 

# Tool - 1 -> will download the news articles from news api
def download_news(_:str) ->str:
    params={
        "api_key":API_KEY,
        "country":COUNTRY,
        "pageSize":ARTICLE_COUNT
    }
    response = requests.get(NEWS_API_URL,params=params)
    response.raise_for_status()
    articles = response.json().get("articles",[])


    for article in articles: # 2 articles will be processed
        processed_result.append(
            {
                "original" : article,
                "reworded" : "",
                "category" : "",
                "hashtags" : ""
            }
        )
    return (f"downloaded {len(processed_result)} successfully")


# Tool 2 : Reword the news article in 2-3 sentences
def reword_news(article_index : str) -> str:
    idx = int(article_index)
    article_text = processed_result[idx]["original"].get("content") or processed_result[idx]["original"].get("description") or processed_result[idx]["original"].get("title")
    
    prompt = f"Reword this news article in 2 -3 sentences for better clarity: \n\n {article_text} "
    response = llm.invoke(prompt)
    reworded = response.content.strip()
    processed_result[idx][reworded] = reworded
    return reworded


# Tool - 3 - Detect the category for article
def detect_category(article_index : str) -> str:
    idx = int(article_index)
    article_text = processed_result[idx]["original"].get("content") or processed_result[idx]["original"].get("description") or processed_result[idx]["original"].get("title")
    prompt= f"Classify this news article into one category like politics,sports,science , tech , health,entertainment:\n\n {article_text} "
    response = llm.invoke(prompt)
    category = response.content.strip()
    processed_result[idx][category] = category
    return category


# Tool - 4 : Generate the hashtags for article
def generate_hashtags(article_index : str) -> str:
    idx = int(article_index)
    article_text = processed_result[idx]["original"].get("content") or processed_result[idx]["original"].get("description") or processed_result[idx]["original"].get("title")
    prompt= f"Generate 3 trending hashtags for this news article : \n\n {article_text} "
    response = llm.invoke(prompt)
    hashtags = response.content.strip()
    processed_result[idx][hashtags] = hashtags
    return hashtags


# Tool 5 - Save the updated article as JSON
def save_to_json() -> str:
    with open (OUTPUT_FILE,"w",encoding="utf-8") as f:
        json.dump(processed_result,f,ensure_ascii=False,indent=4)
    return f"Saved {len(processed_result)} results to the {OUTPUT_FILE}"

#Register the tools with langchain
tools=[
    
    Tool(
        name = "Download news",
        func = download_news,
        description="Fetch the latest news articles from the news api"
    ),
    Tool(
        name = "Reword News",
        func = reword_news,
        description="Reword the news at given numeric index(string of an integer,'0'.)"
    ),
    Tool(
        name = "Detect Category",
        func = detect_category,
        description="Detect the category of news article at given numeric index"
    ),
    Tool(
        name = "Generate Hashtags",
        func = generate_hashtags,
        description="Genarate the hashtags for the news at given numeric index"

    ),
    Tool(
        name = "Save to JSON",
        func = save_to_json,
        description="save the processed articles to json file"
        
    ) 
]



# memory for agent (conversation)

memory = ConversationBufferMemory(
    memory_key= "chat_history",
    return_messages= True  #to refer the memory
)
"""
#define agent
use tools,memory to achive goals
"""
agent = initialize_agent(

    tools= tools,
    llm= llm,
    memory = memory,
    verbose = True,
    agent="zero-shot-react-description"
)

goal = f"""

Download the latest {ARTICLE_COUNT} news articles from the US.
For each article index (o to {ARTICLE_COUNT-1}) 
       1. Call 'Reword News' with the index number as a string.
       2. Call 'Detect Category' with the same index,
       3. Call 'Generate Hashtags' with the same index.
After all the articles are processed,call 'Save to JSON'
"""


result =agent.run(goal)

print("\n News agent execution completed \n {result}")
