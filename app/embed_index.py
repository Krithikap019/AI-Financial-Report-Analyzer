# embed_index.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

DEFAULT_MODEL = "all-MiniLM-L6-v2"

def load_embedder(model_name: str = DEFAULT_MODEL):
    return SentenceTransformer(model_name)

def embed_texts(embedder, texts):
    emb = embedder.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return emb.astype("float32")

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)  # cosine similarity
    index.add(embeddings)
    return index