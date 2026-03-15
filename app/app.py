# # app.py
# # Single-file Streamlit AI Financial Report Analyzer (RAG MVP)
# # - Upload PDF/TXT
# # - Extract text (PDF page-aware)
# # - Chunk + embed (sentence-transformers)
# # - FAISS retrieval
# # - If OPENAI_API_KEY is set: generates an answer with citations
# # - If not set: shows the best matching evidence chunks (still useful)

# import os
# import re
# import tempfile
# from dataclasses import dataclass
# from typing import List, Dict, Any, Tuple

# import streamlit as st

# # --- Optional / graceful imports ---
# try:
#     import fitz  # PyMuPDF
# except Exception as e:
#     fitz = None

# try:
#     import faiss
# except Exception as e:
#     faiss = None

# try:
#     import numpy as np
# except Exception as e:
#     np = None

# try:
#     from sentence_transformers import SentenceTransformer
# except Exception as e:
#     SentenceTransformer = None


# # -----------------------------
# # Config
# # -----------------------------
# APP_TITLE = "AI Financial Report Analyzer (Single-file RAG)"
# DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"
# CHUNK_WORDS = 350         # chunk size in words (simple + fast)
# CHUNK_OVERLAP = 80        # overlap in words
# TOP_K_RETRIEVE = 6        # retrieve this many chunks
# TOP_K_CONTEXT = 4         # send this many chunks to the LLM
# MAX_CHARS_PER_CHUNK_IN_PROMPT = 1200  # truncate chunks in prompt to control tokens


# # -----------------------------
# # Data structures
# # -----------------------------
# @dataclass
# class Chunk:
#     doc_id: str
#     page: int
#     chunk_id: str
#     text: str


# # -----------------------------
# # Helpers: extraction
# # -----------------------------
# def extract_txt(file_path: str) -> List[Dict[str, Any]]:
#     with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#         text = f.read()
#     return [{"page": 1, "text": text}]


# def extract_pdf_pages(file_path: str) -> List[Dict[str, Any]]:
#     if fitz is None:
#         raise RuntimeError("PyMuPDF (fitz) is not installed. Install with: pip install pymupdf")

#     doc = fitz.open(file_path)
#     pages = []
#     for i, page in enumerate(doc):
#         txt = page.get_text("text") or ""
#         pages.append({"page": i + 1, "text": txt})
#     return pages


# def clean_text(s: str) -> str:
#     s = s.replace("\x00", " ")
#     s = re.sub(r"[ \t]+", " ", s)
#     s = re.sub(r"\n{3,}", "\n\n", s)
#     return s.strip()


# # -----------------------------
# # Helpers: chunking
# # -----------------------------
# def chunk_words(text: str, chunk_size: int = CHUNK_WORDS, overlap: int = CHUNK_OVERLAP) -> List[str]:
#     words = text.split()
#     if not words:
#         return []

#     chunks = []
#     i = 0
#     step = max(1, chunk_size - overlap)
#     while i < len(words):
#         chunk = " ".join(words[i : i + chunk_size])
#         if chunk.strip():
#             chunks.append(chunk)
#         i += step
#     return chunks


# def chunk_pages(pages: List[Dict[str, Any]], doc_id: str) -> List[Chunk]:
#     out: List[Chunk] = []
#     for p in pages:
#         page_num = int(p.get("page", 1))
#         text = clean_text(p.get("text", ""))
#         for idx, c in enumerate(chunk_words(text)):
#             out.append(
#                 Chunk(
#                     doc_id=doc_id,
#                     page=page_num,
#                     chunk_id=f"{doc_id}_p{page_num}_c{idx}",
#                     text=c,
#                 )
#             )
#     return out


# # -----------------------------
# # Embeddings + FAISS
# # -----------------------------
# @st.cache_resource
# def load_embedder(model_name: str = DEFAULT_EMBED_MODEL):
#     if SentenceTransformer is None:
#         raise RuntimeError("sentence-transformers is not installed. Install with: pip install sentence-transformers")
#     return SentenceTransformer(model_name)


# def embed_texts(embedder, texts: List[str]):
#     if np is None:
#         raise RuntimeError("numpy is not installed.")
#     emb = embedder.encode(texts, show_progress_bar=False, convert_to_numpy=True)
#     return emb.astype("float32")


# def build_faiss_index(embeddings):
#     if faiss is None:
#         raise RuntimeError("faiss is not installed. Install with: pip install faiss-cpu")
#     dim = embeddings.shape[1]
#     index = faiss.IndexFlatIP(dim)  # cosine similarity after L2-normalization
#     faiss.normalize_L2(embeddings)
#     index.add(embeddings)
#     return index


# def retrieve_chunks(embedder, index, chunks: List[Chunk], query: str, top_k: int = TOP_K_RETRIEVE) -> List[Tuple[float, Chunk]]:
#     q_emb = embed_texts(embedder, [query])
#     faiss.normalize_L2(q_emb)
#     D, I = index.search(q_emb, top_k)
#     results: List[Tuple[float, Chunk]] = []
#     for score, idx in zip(D[0], I[0]):
#         if idx < 0:
#             continue
#         results.append((float(score), chunks[int(idx)]))
#     return results


# # -----------------------------
# # LLM (OpenAI) - optional
# # Supports both new and legacy OpenAI SDKs.
# # -----------------------------
# def openai_answer(question: str, context_items: List[Tuple[float, Chunk]]) -> str:
#     api_key = os.getenv("OPENAI_API_KEY", "").strip()
#     if not api_key:
#         raise RuntimeError("OPENAI_API_KEY is not set.")

#     context_blocks = []
#     for score, c in context_items:
#         snippet = c.text[:MAX_CHARS_PER_CHUNK_IN_PROMPT]
#         context_blocks.append(f"[{c.doc_id}:{c.page}] {snippet}")

#     system = (
#         "You are a careful financial analyst assistant.\n"
#         "Use ONLY the provided CONTEXT to answer.\n"
#         "If the answer isn't in the context, say: 'Not available in provided document.'\n"
#         "Always cite sources inline like [doc:page].\n"
#         "Keep the answer concise.\n"
#     )
#     user = "CONTEXT:\n" + "\n\n".join(context_blocks) + f"\n\nQUESTION: {question}"

#     # Try new SDK first
#     try:
#         from openai import OpenAI
#         client = OpenAI(api_key=api_key)
#         resp = client.chat.completions.create(
#             model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
#             messages=[
#                 {"role": "system", "content": system},
#                 {"role": "user", "content": user},
#             ],
#             temperature=0.1,
#             max_tokens=450,
#         )
#         return resp.choices[0].message.content
#     except Exception:
#         pass

#     # Fallback: legacy SDK
#     try:
#         import openai
#         openai.api_key = api_key
#         resp = openai.ChatCompletion.create(
#             model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
#             messages=[
#                 {"role": "system", "content": system},
#                 {"role": "user", "content": user},
#             ],
#             temperature=0.1,
#             max_tokens=450,
#         )
#         return resp["choices"][0]["message"]["content"]
#     except Exception as e:
#         raise RuntimeError(f"OpenAI call failed: {e}")


# # -----------------------------
# # Streamlit UI
# # -----------------------------
# st.set_page_config(page_title=APP_TITLE, layout="wide")
# st.title(APP_TITLE)

# with st.expander("Setup / Requirements", expanded=False):
#     st.markdown( """
# **Install dependencies:**
# ```bash
# pip install streamlit pymupdf sentence-transformers faiss-cpu numpy openai""")

