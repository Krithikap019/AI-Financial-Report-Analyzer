import os
from openai import OpenAI
from prompts import build_prompt

def generate_answer(chunks, question):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY not set. Showing retrieved chunks only."

    client = OpenAI(api_key=api_key)

    prompt = build_prompt(chunks, question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content