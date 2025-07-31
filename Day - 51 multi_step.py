from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSequence

# LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# Prompts
pitch_prompt = ChatPromptTemplate.from_template(
    "Write a 2 sentence marketing pitch for the product {product_name}"
)

tweet_prompt = ChatPromptTemplate.from_template(
    "Convert the following pitch into a single twitter post (under 200 characters):\n{pitch}"
)

hashtag_prompt = ChatPromptTemplate.from_template(
    "Suggest 3 trending hashtags for this tweet:\n{tweet}"
)

# Step 1: Get marketing pitch
step1 = (
    pitch_prompt
    | llm
    | RunnableLambda(lambda msg: {
        "pitch": msg.content if hasattr(msg, "content") else str(msg)
    })
    # combine pitch back with original input (which contains product_name)
    | RunnableLambda(lambda x: {
        "product_name": input_data["product_name"],
        "pitch": x["pitch"]
    })
)

# Step 2: Convert pitch -> tweet (carry all data forward)
# Step 2: Convert pitch -> tweet
step2 = (
    RunnableLambda(lambda x: {"pitch": x["pitch"]})
    | tweet_prompt
    | llm
    | RunnableLambda(lambda msg: msg.content if hasattr(msg, "content") else str(msg))  # ✅ fixed
    | RunnableLambda(lambda tweet: lambda x: {
        "product_name": x["product_name"],
        "pitch": x["pitch"],
        "tweet": tweet
    })
)


# Step 3: Generate hashtags from tweet
step3 = (
    RunnableLambda(lambda x: {"tweet": x["tweet"]})
    | hashtag_prompt
    | llm
    | RunnableLambda(lambda msg: msg.content if hasattr(msg, "content") else str(msg))  # ✅ clean extract
    | RunnableLambda(lambda hashtags: lambda x: {
        "product_name": x["product_name"],
        "pitch": x["pitch"],
        "tweet": x["tweet"],
        "hashtag": hashtags
    })
)


# Chain
chain = RunnableSequence(
    first=step1,
    middle=[step2],
    last=step3
)

# Run
input_data = {"product_name": "Dell HP AI powered Laptop"}
final_output = chain.invoke(input_data)

# Output
print("Pitch:", final_output["pitch"])
print("Tweet:", final_output["tweet"])
print("Hashtags:", final_output["hashtag"])
