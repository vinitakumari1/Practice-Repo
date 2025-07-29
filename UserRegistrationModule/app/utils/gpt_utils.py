from openai import OpenAI
import os


client = OpenAI (api_key = os.getenv("OPENAI_API_KEY"))




def explain_password_strength(password: str):
    prompt = f"Is the password '{password}' weak or strong? Briefly explain. Start with 'Weak:' or 'Strong:'."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
