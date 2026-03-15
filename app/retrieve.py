import faiss

def retrieve(query, embedder, index, chunks, top_k=5):
    q_embedding = embedder.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(q_embedding)
    D, I = index.search(q_embedding, top_k)

    results = []
    for idx in I[0]:
        results.append(chunks[idx])
    return results