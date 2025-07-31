# Problem startament : Write an python program which will demo the langchain - single step chain

#Sample Text 
#Patient complains  of frequent headaches over the past two weeks,especially in the morinings.
#No history of trauma.Blood pressure normal . Advised to reduce scren time and stay hydrated.

#Patient Summary : 
# You've been experiencing headaches quite often over
#  the past two weeks, particularly in the mornings. 
# There's no evidence that these headaches are due to any injury.
#  Your blood pressure is also normal. I recommend that you try 
# to cut down on the amount of time you spend looking at screens 
# and make sure you're drinking enough water.

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate,HumanMessagePromptTemplate

#chatprompttemplate rmeebrs the history unline prompttemplate


#Init LLM
llm = ChatOpenAI(model="gpt-4", temperature = 0.3)

# Basic transcript
transcript = """
Patient complains  of frequent headaches over the past two weeks,especially in the morinings.
No history of trauma.Blood pressure normal . Advised to reduce scren time and stay hydrated."""



#System Prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an clinical AI assistnat.Generate a ptient friendly summary from the provided transcript."
)

#Human Prompt
human_prompt = HumanMessagePromptTemplate.from_template(
    "transcript : {transcript_text}")  #bound text will come from outside dont use f string



#Build the chat prompt
Chat_prompt = ChatPromptTemplate.from_messages([system_prompt,human_prompt])


# set up chain  between LLM and prompt
chain = LLMChain(llm= llm, prompt = Chat_prompt)


response = chain.run({"transcript_text": transcript}) 

print(f"Patient Summary : {response}")