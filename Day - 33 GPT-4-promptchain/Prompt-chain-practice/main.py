import os
from openai import OpenAI
from app.api.chain import TextInput
from fastapi import FastAPI

app=FastAPI()

client = OpenAI (api_key = os.getenv("OPENAI_API_KEY")) # always read from Enviroments

@app.post("/prompt_chain")
async def prompt_chain(data:TextInput):
    
    summary = client.chat.completions.create (
        model = "gpt-4", 
        messages = [
            {"role": "system", "content" : "Summarize the following text"},
            {"role" : "user","content" : data.text}
        ], 
        temperature = 0.4
    ).choices[0].message.content.strip()
    

    # Step 2 : Grammar Fix
    
    improved_text = client.chat.completions.create (
    model = "gpt-4", 
    messages = [
        {"role": "system", "content" : "Improve grammar and clarity of this text"},
        {"role" : "user","content" : data.text}
    ], 
    temperature = 0.3
).choices[0].message.content.strip()

    # Step 3 : Translate
    translated_text = client.chat.completions.create (
    model = "gpt-4", 
    messages = [
        {"role": "system", "content" : f"Translate the following text to {input.language}."},
        {"role" : "user","content" : improved_text}
    ], 
    temperature = 0.3
    ).choices[0].message.content.strip()

    return {
        "summary" : summary,
        "improved_text" : improved_text,
        "translated_text" : translated_text
    }

    


   