def build_prompt(context_chunks, question):
    context = ""
    for chunk in context_chunks:
        context += f"[{chunk['doc_id']} page {chunk['page']}]\n{chunk['text']}\n\n"

    prompt = f"""
You are a financial analyst assistant.
Answer using ONLY the context below.
If not found, say: Not available in provided document.
Always cite like [doc page X].

Context:
{context}

Question:
{question}

Answer:
"""
    return prompt