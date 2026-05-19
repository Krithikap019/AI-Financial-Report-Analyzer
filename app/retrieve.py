import faiss
import numpy as np

def retrieve(query, embedder, index, chunks, top_k=5):
    q_embedding = embedder.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(q_embedding)
    D, I = index.search(q_embedding, top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        if idx < len(chunks):
            chunk = chunks[idx].copy()
            chunk["confidence"] = float(score)
            results.append(chunk)

    results = sorted(results, key=lambda x: x["confidence"], reverse=True)
    return results