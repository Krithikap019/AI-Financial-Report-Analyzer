import os
import tempfile
import streamlit as st

from ingest import extract_pdf_pages, extract_txt
from chunk import chunk_pages
from embed_index import load_embedder, embed_texts, build_faiss_index
from retrieve import retrieve
from generate import generate_answer

st.title("AI Financial Report Analyzer")

uploaded = st.file_uploader("Upload 10-K / transcript", type=["pdf", "txt"])

if uploaded and st.button("Index Document"):
    suffix = "." + uploaded.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        file_path = tmp.name

    if suffix == ".pdf":
        pages = extract_pdf_pages(file_path)
    else:
        pages = extract_txt(file_path)

    chunks = chunk_pages(pages, uploaded.name)

    embedder = load_embedder()
    embeddings = embed_texts(embedder, [c["text"] for c in chunks])
    index = build_faiss_index(embeddings)

    st.session_state["chunks"] = chunks
    st.session_state["index"] = index
    st.session_state["embedder"] = embedder

    st.success("Document indexed successfully!")

question = st.text_input("Ask a question about the report")

if st.button("Ask") and question:
    if "index" not in st.session_state:
        st.error("Please index a document first.")
    else:
        retrieved = retrieve(
            question,
            st.session_state["embedder"],
            st.session_state["index"],
            st.session_state["chunks"]
        )

        answer = generate_answer(retrieved, question)

        st.markdown("### Answer")
        st.write(answer)

        st.markdown("### Retrieved Evidence")
        for r in retrieved:
            st.write(f"[{r['doc_id']} page {r['page']}]")
            st.write(r["text"][:500] + "...")