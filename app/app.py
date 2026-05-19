import os
import tempfile
import streamlit as st
from ingest import extract_pdf_pages, extract_txt
from chunk import chunk_pages
from embed_index import load_embedder, embed_texts, build_faiss_index
from retrieve import retrieve
from generate import generate_answer, generate_summary, generate_sentiment

st.set_page_config(
    page_title="AI Financial Report Analyzer",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main { padding: 1rem 2rem; }
    .stButton > button {
        background-color: #0a7c52;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #064d33; }
    .chat-message { padding: 1rem; border-radius: 8px; margin: 0.5rem 0; }
    .user-message { background: #edf5f1; border-left: 3px solid #0a7c52; }
    .assistant-message { background: #f8f9fa; border-left: 3px solid #6c757d; }
    .source-badge { background: #d4ede5; color: #064d33; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin: 2px; display: inline-block; }
    .stat-card { background: #edf5f1; border-radius: 8px; padding: 1rem; text-align: center; border: 1px solid rgba(10,124,82,0.15); }
    .stat-num { font-size: 1.8rem; font-weight: 700; color: #0a7c52; }
    .stat-label { font-size: 0.75rem; color: #3a5a4a; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

QUICK_QUESTIONS = [
    "What was the total revenue?",
    "What are the key risk factors?",
    "What is the net income?",
    "What are the main business segments?",
    "What is the revenue growth year over year?",
    "What does management say about future outlook?",
    "What are the operating expenses?",
    "What is the cash flow from operations?",
]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed" not in st.session_state:
    st.session_state.indexed = False
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {}
if "summary" not in st.session_state:
    st.session_state.summary = None
if "sentiment" not in st.session_state:
    st.session_state.sentiment = None

with st.sidebar:
    st.markdown("## 📊 Financial Analyzer")
    st.markdown("---")
    uploaded = st.file_uploader("Upload 10-K / Transcript", type=["pdf", "txt"])

    if uploaded and st.button("🔍 Index Document", use_container_width=True):
        suffix = "." + uploaded.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.getbuffer())
            file_path = tmp.name

        progress = st.progress(0)
        status = st.empty()

        status.text("📄 Extracting text...")
        progress.progress(10)
        if suffix == ".pdf":
            pages = extract_pdf_pages(file_path)
        else:
            pages = extract_txt(file_path)

        status.text("✂️ Chunking document...")
        progress.progress(30)
        chunks = chunk_pages(pages, uploaded.name)

        status.text("🧠 Generating embeddings...")
        progress.progress(55)
        embedder = load_embedder()
        embeddings = embed_texts(embedder, [c["text"] for c in chunks])

        status.text("🗂️ Building FAISS index...")
        progress.progress(75)
        index = build_faiss_index(embeddings)

        status.text("📝 Generating summary...")
        progress.progress(85)
        all_text = " ".join([c["text"] for c in chunks[:20]])
        summary = generate_summary(all_text)
        sentiment = generate_sentiment(all_text)

        st.session_state["chunks"] = chunks
        st.session_state["index"] = index
        st.session_state["embedder"] = embedder
        st.session_state["indexed"] = True
        st.session_state["chat_history"] = []
        st.session_state["summary"] = summary
        st.session_state["sentiment"] = sentiment
        st.session_state["doc_stats"] = {
            "name": uploaded.name,
            "pages": len(pages),
            "chunks": len(chunks),
            "words": sum(len(c["text"].split()) for c in chunks),
        }

        progress.progress(100)
        status.text("✅ Done!")
        st.success("Document indexed successfully!")

    if st.session_state.indexed:
        st.markdown("---")
        st.markdown("### 📁 Document")
        stats = st.session_state.doc_stats
        st.markdown(f"**{stats['name']}**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='stat-card'><div class='stat-num'>{stats['pages']}</div><div class='stat-label'>Pages</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'><div class='stat-num'>{stats['chunks']}</div><div class='stat-label'>Chunks</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

st.title("📊 AI Financial Report Analyzer")
st.markdown("*Upload a 10-K filing or earnings transcript and ask questions about it.*")

if not st.session_state.indexed:
    st.info("👈 Upload a financial document in the sidebar to get started.")
    st.markdown("""
    ### What you can do:
    - 📄 Upload **10-K filings**, earnings transcripts, or annual reports
    - 💬 Ask natural language questions about the document
    - 🔍 Get **citation-backed answers** from specific pages
    - 📊 Auto-generated **document summary** and **sentiment analysis**
    - ⚡ Use **quick question templates** for common financial queries
    """)
else:
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📋 Summary", "📊 Sentiment"])

    with tab1:
        st.markdown("### Quick Questions")
        cols = st.columns(4)
        for i, q in enumerate(QUICK_QUESTIONS):
            with cols[i % 4]:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    st.session_state["pending_question"] = q

        st.markdown("---")

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-message user-message'>🧑 <strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message assistant-message'>🤖 <strong>Assistant:</strong> {msg['content']}</div>", unsafe_allow_html=True)
                if "sources" in msg:
                    st.markdown("**Sources:**")
                    for s in msg["sources"]:
                        st.markdown(f"<span class='source-badge'>📄 {s['doc_id']} — Page {s['page']}</span>", unsafe_allow_html=True)
                    with st.expander("View retrieved evidence"):
                        for s in msg["sources"]:
                            st.markdown(f"**[{s['doc_id']} — Page {s['page']}]**")
                            st.markdown(s["text"][:600] + "...")
                            st.markdown("---")

        question = st.chat_input("Ask a question about the report...")

        if "pending_question" in st.session_state:
            question = st.session_state.pop("pending_question")

        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Retrieving relevant sections and generating answer..."):
                retrieved = retrieve(
                    question,
                    st.session_state["embedder"],
                    st.session_state["index"],
                    st.session_state["chunks"]
                )
                answer = generate_answer(retrieved, question, st.session_state.chat_history)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "sources": retrieved
            })
            st.rerun()

    with tab2:
        st.markdown("### 📋 Document Summary")
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
        else:
            st.info("Summary will appear after indexing a document.")

    with tab3:
        st.markdown("### 📊 Sentiment Analysis")
        if st.session_state.sentiment:
            st.markdown(st.session_state.sentiment)
        else:
            st.info("Sentiment analysis will appear after indexing a document.")