"""
Write an agent which will accept the goal
- accept a task
- Choose the steps
- Usage of tools to perform sub tasks
- Remebers the result and actions during conversation
"""

#Import langchain modules for agent creation

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent,Tool
from langchain.memory import ConversationBufferMemory

#create and init LLM
llm= ChatOpenAI(
    model="gpt-4",
    temperature = 0.3
)
 
# Goal -> Tool -> Generate the marketing pitch

def generate_pitch(product_name:str) -> str:
    prompt = f"Write a 2 sentence marketing pitch for the product {product_name}"  # f is written because product_name is coming from function, not a bound parameter
    response = llm.invoke(prompt) # Call llm and get the response
    return response.content #extract the reply or content from the model response


#Goal -> Tool -> Get the tweet based on the pitch

def pitch_to_tweet(pitch:str) -> str:
    prompt=f"Convert this pitch into a single twitter post (under 200 characters) : {pitch}"
    response = llm.invoke(prompt)
    return response.content



# Goal -> Get hasghtag based on tweet

def tweet_to_hashtags(tweet:str) -> str:
    prompt = f"suggest 3 trending hashtags for this tweet : {tweet}"
    response = llm.invoke(prompt)
    return response.content



# Register the tools with Langchain

tools= [
    Tool(
        name = "Generate Pitch",
        func = generate_pitch,
        description="Creates a 2 sentence marketing pitch from a product name"
    ),
    Tool(
        name = "Pitch to Tweet",
        func = pitch_to_tweet,
        description="Convert the marketing pitch into tweet"
    ),
    Tool(
        name = "Tweet to Hashtag",
        func = tweet_to_hashtags,
        description="Suggests trending hashtags for the given tweet"
    )
    
]



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

#Define the goal for agent 
goal = "Generate a pitch,then a tweet,then hashtags for 'Dell HP AI powered Laptop "


#assign goal and run the agent 
result = agent.run(goal)

print(result)