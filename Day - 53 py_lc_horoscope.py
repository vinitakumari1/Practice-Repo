"""
Autonomous horoscope processing agent using langchain

-Downloads 




""" 


HOSROSCOPE_API_URL ="https://ohmanda.com/api/horoscope/"

SIGNS=[
"aquarius","aries","taurus","gemini","cancer","leo",
"virgo","libra","scorpio","sagittarius","capricorn","pisces"
]

OUTPUT_FILE = "Day_53_horoscope_summary.json"
from colorama import init, Fore, Style

# Initialize color support on Windows terminals
init(autoreset=True)

import requests
import json


from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent,Tool
from langchain.memory import ConversationBufferMemory

processed_results =[]
#===========================
# setup llm - openai -gpt4 
#===========================

llm= ChatOpenAI(
    model="gpt-4",
    temperature = 0.3
)
#=========================
#Tools
# 1. download horoscopes
# 2. reword horoscope
# 3. genrate keyword
# 4. detect sentiment
# 5. create summary
# 6. Save to json
#===========================

#Tool 1 - download_horoscopes

def download_horoscopes(_: str) -> str:
    for sign in SIGNS:
         url = f"{HOSROSCOPE_API_URL}{sign}/"
         response = requests.get(url)
         if response.status_code == 200 :
              processed_results.append(
                   {
                        "sign":sign,
                        "original":response.json(),
                        "reworded":"",
                        "keywords":"",
                        "sentiment":"",
                        "summary":""

                   }
                )
              
    return f"Downloaded horoscopes for {len(processed_results)} zodiac signs"

#Tool - 2 : Reword_horoscopes

def reword_horoscopes(index : str) -> str:
    idx = int(index.strip().replace('"', ''))

    original_horoscope = processed_results[idx]["original"]["horoscope"]
    prompt = f"Reword this horoscope in 2 to 3 sentences for clarity :\n\n {original_horoscope}"
    reworded_horoscope = llm.invoke(prompt).content.strip()
    processed_results[idx]["reworded"] = reworded_horoscope
    return reworded_horoscope

#Tool - 3 : generate_keyword

def generate_keyword(index : str) -> str:
    idx = int(index.strip().replace('"', ''))

    original_horoscope = processed_results[idx]["original"]["horoscope"]
    prompt = f"Extract 3-5 keywords from this horoscope:\n\n {original_horoscope}"
    keywords = llm.invoke(prompt).content.strip()
    processed_results[idx]["keywords"] = keywords
    return keywords



#Tool - 4 : Detect sentiment

def detect_sentiment(index : str) -> str:
    idx = int(index.strip().replace('"', ''))

    original_horoscope = processed_results[idx]["original"]["horoscope"]
    prompt = f"Is this horoscope overall Positive, Negative or Neutral ? Respond with one word only:\n\n {original_horoscope}"
    sentiment = llm.invoke(prompt).content.strip()
    processed_results[idx]["sentiment"] = sentiment
    return sentiment


# Tool - 5 : Create summary 

def create_summary(index : str) -> str:
    idx = int(index.strip().replace('"', ''))

    original_horoscope = processed_results[idx]["original"]["horoscope"]
    prompt = f"Summarize this horoscope in a one short sentence :\n\n {original_horoscope}"
    summary = llm.invoke(prompt).content.strip()
    processed_results[idx]["summary"] = summary
    return summary


# Tool - 6 : Save to json

def save_to_json(_:str) -> str:
    with open (OUTPUT_FILE,"w",encoding="utf-8") as f:
        json.dump(processed_results,f,ensure_ascii=False,indent=4)
    return f"Saved {len(processed_results)} results to the {OUTPUT_FILE}"


#=====================================================
# Register the tools with langchain and Setup the Tool Chain
#=====================================================

tools=[
    
    Tool(
        name = "Download Horoscopes",
        func = download_horoscopes,
        description="Fetch today's horoscope for all 12 zodiac signs."
    ),
    Tool(
        name = "Reword Horoscopes",
        func = reword_horoscopes,
        description="Reword the horoscope at a given numeric index.)"
    ),
    Tool(
        name = "Generate Keyword",
        func = generate_keyword,
        description="Generate keyword for the horoscope at a given numeric index."
    ),
    Tool(
        name = "Detect Sentiment",
        func = detect_sentiment,
        description="Detect sentiment for the horoscope at given numeric index."

    ),
    Tool(
        name = "Create summary",
        func = create_summary,
        description="Create a short summary for the horoscope at given numeric inde."

    ),

    Tool(
        name = "Save to JSON",
        func = save_to_json,
        description="Save the processed horoscopes to json file"
        
    ) 
]



#================================
#  memory for agent (conversation)
#=================================


memory = ConversationBufferMemory(
    memory_key= "chat_history",  #to remeber the conversation while resoning
    return_messages= True  #to refer the memory
)

"""
#define agent
use tools,memory to achive goals
"""

#==========================================
#  Initialize Agent - with tools and memory
#==========================================
agent = initialize_agent(

    tools= tools,
    llm= llm,
    memory = memory,
    verbose = True,
    agent="zero-shot-react-description",
    max_iterations =100 
)


#==========================================
#  Goal
#==========================================
goal = f"""

Download today's horoscopes for 12 zodiac signs.
For each index (0 to len{SIGNS} - 1) 
       1. Call 'Reword Horoscopes' with the index.
       2. Call 'Generate Keyword' with the index.
       3. Call 'Detect Sentiment' with the index.
       4. Call 'Create summary' with the index.
      
After all the horoscopes are processed,call 'Save to JSON'.
 When done, respond ONLY with : PROCESSING_COMPLETED
"""


#result =agent.run(goal)

agent.invoke(
       {"input": goal},
       handle_parsing_errors=True
)

print("\n Horoscopes processing completed")

