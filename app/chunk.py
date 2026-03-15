def chunk_text(text, chunk_size=400, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def chunk_pages(pages, doc_id):
    all_chunks = []
    for page in pages:
        chunks = chunk_text(page["text"])
        for idx, c in enumerate(chunks):
            all_chunks.append({
                "doc_id": doc_id,
                "page": page["page"],
                "text": c
            })
    return all_chunks