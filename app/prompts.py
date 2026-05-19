def build_prompt(context_chunks, question):
    context = ""
    for chunk in context_chunks:
        context += f"[{chunk['doc_id']} page {chunk['page']}]\n{chunk['text']}\n\n"

    prompt = f"""You are a financial analyst assistant.
Answer using ONLY the context below.
If the answer is not found, say: "Not available in the provided document."
Always cite your sources like [filename page X].
Be concise, precise, and professional.

Context:
{context}

Question: {question}

Answer:"""
    return prompt

def build_summary_prompt(text):
    return f"""Analyze this financial document and provide a structured summary with the following sections:

## Executive Overview
(2-3 sentences about the company and document)

## Key Financial Highlights
(bullet points of the most important financial metrics)

## Business Overview
(main business segments and operations)

## Key Risks
(top 3-5 risk factors mentioned)

## Forward Outlook
(management's guidance and future expectations)

Document text:
{text}"""

def build_sentiment_prompt(text):
    return f"""Analyze the tone and sentiment of this financial document. Provide:

## Overall Sentiment
(Positive / Neutral / Negative with explanation)

## Management Tone
(How management discusses the business - confident, cautious, optimistic, defensive?)

## Key Positive Signals
(bullet points of positive language and metrics)

## Key Risk Signals
(bullet points of concerning language or risk factors)

## Sentiment Score
(Rate overall sentiment: 1-10, where 1 is very negative and 10 is very positive)

Document text:
{text}"""