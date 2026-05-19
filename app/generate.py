import os
from openai import OpenAI
from prompts import build_prompt, build_summary_prompt, build_sentiment_prompt

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def generate_answer(chunks, question, chat_history=None):
    client = get_client()
    if not client:
        return "⚠️ OPENAI_API_KEY not set. Showing retrieved chunks only."

    prompt = build_prompt(chunks, question)
    messages = [{"role": "system", "content": "You are a financial analyst assistant. Answer only from the provided context. Always cite sources like [doc page X]. Be concise and precise."}]

    if chat_history:
        for msg in chat_history[-6:]:
            if msg["role"] in ["user", "assistant"]:
                messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1,
    )
    return response.choices[0].message.content

def generate_summary(text):
    client = get_client()
    if not client:
        return "⚠️ OPENAI_API_KEY not set."

    prompt = build_summary_prompt(text[:6000])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial analyst. Summarize the document clearly and concisely."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content

def generate_sentiment(text):
    client = get_client()
    if not client:
        return "⚠️ OPENAI_API_KEY not set."

    prompt = build_sentiment_prompt(text[:6000])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial sentiment analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content