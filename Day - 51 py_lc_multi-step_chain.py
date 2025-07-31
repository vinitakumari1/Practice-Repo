#Product - Dell Laptop
# Step 1 - Write a marketing pitch for the product {product_name}
# Step 2 - Convert the pitch into a single twitter post (under 200 characters)
# Step 3 - Build 3 hashtags for this tweet

# General
# What is RunnableLambda -> Which wraps any Lambda, function
# what is RunnableSequence -> Runs multiple runnables in a order



#Runnbale -> Invoke  -> step
#each step will have a prompt


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSequence 



llm = ChatOpenAI(model="gpt-4", temperature = 0.3)


pitch_prompt = ChatPromptTemplate.from_template(
    "Write a 2 sentence marketing pitch for the product {product_name}"
)


tweet_prompt = ChatPromptTemplate.from_template(
    "convert the following pitch into a single twitter post(under 200 characters) : \n {pitch}"
)

hashtag_prompt = ChatPromptTemplate.from_template(
    "Suggest 3 trending hastags for this tweet \n {tweet} "
)
input_data = {"product_name": "Dell HP AI powered Laptop"}
#  Step 1 
#A chain step is created---
# 1. Use pitch_prompt to format the user input into a complete prompt statemnt
# 1. Write a marketing pitch for the product "Dell HP AI powered Laptop"
#2. Send the pormpt to llm
# 3. Captutre the LLM output with lambda so that we have a dict {dict of product_name and pitch}


# output of step 1 is a dictinory of productname and pitch
step1 = (
    pitch_prompt | llm | RunnableLambda(
        lambda msg : {
            "product_name": input_data["product_name"],
            "pitch": msg.content if hasattr(msg,"content") else str(msg)
        }
    )
)

#step2 - for generating tweet from pitch(step1)
# 1. Pass the pitch text(step 1 output)
# 2. format it with tweet prompt
# 2. Convert the pitch into a single twitter post (under 200 characters) 
#3. Send this to llm
# 4. Store pitch and tweet (response from llm) 



step2=(
   RunnableLambda(
        lambda x:{"pitch" : x["pitch"]} # extract the pitch from step 1
         |tweet_prompt
         |llm
         |RunnableLambda(
             lambda msg:{
                 "pitch": input_data["pitch"], #get from step 1
                 "tweet" : msg.content if hasattr(msg,"content") else str(msg)
             }
         )

    )
)

#Step3 - get the hashtags from the tweet(step2)
#1. Pass the tweet text 
# 2 . format the tweet prompt
# 3. example : suggest 3 tredning hanshtags for this tweet (bla bla bla)
# 4.send to llm
#5.store pitch,tweet text,hashtag. from the llm output



step3= (
    RunnableLambda( lambda x: {"tweet" : x["tweet"]})
    | hashtag_prompt
    |llm 
    | RunnableLambda(
        lambda msg:{
            "pitch": input_data["pitch"],
            "tweet":input_data["tweet"],
            "hashtag": msg.content if hasattr(msg,"content") else str(msg)
        }
    )
)

# all these 3 steps are tasks 


chain = RunnableSequence(
    first= step1,
    middle= [step2],  # if more than 3 steps write middle=[step2,step3,step4]
    last= step3   
)

input_data = {"product_name": "Dell HP AI powered Laptop"}


step1_output = step1.invoke(input_data)
input_data["pitch"] = step1_output["pitch"]


step2_output = step2.invoke(input_data)
input_data["pitch"] = step1_output["pitch"]

step3_output = step3.invoke(input_data)

print("Pitch:", input_data["pitch"])
print("Tweet:", input_data["tweet"])
print("Hashtag:", step3_output.get("hashtag"))