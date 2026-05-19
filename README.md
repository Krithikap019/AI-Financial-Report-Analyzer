# 📊 AI Financial Report Analyzer

An intelligent RAG-based system that transforms long financial documents into a searchable, conversational assistant. Upload a 10-K filing or earnings transcript and ask questions in plain English — get citation-backed answers instantly.

## 🚀 Live Demo
[View on Streamlit](https://your-streamlit-url.streamlit.app)

## 🧠 What It Does

Instead of manually reading through hundreds of pages of financial filings, users can:
- Ask natural language questions like *"What was revenue growth?"* or *"What are the key risks?"*
- Get precise, citation-backed answers grounded in the document
- View an auto-generated executive summary
- Analyze document sentiment and management tone
- Use quick question templates for common financial queries

## ⚙️ How It Works

```
PDF / TXT Upload
      ↓
Text Extraction (PyMuPDF)
      ↓
Overlapping Chunking (400 words, 100 overlap)
      ↓
Semantic Embeddings (SentenceTransformer: all-MiniLM-L6-v2)
      ↓
FAISS Vector Index (cosine similarity)
      ↓
Query → Embedding → Top-K Retrieval
      ↓
LLM Answer Generation (GPT-4o-mini) with citations
```

## ✨ Features

- **Chat interface** with conversation memory
- **Auto document summary** on upload
- **Sentiment analysis** — overall tone, management confidence, risk signals
- **Quick question templates** for common financial queries
- **Source citations** with page references
- **Confidence scoring** on retrieved chunks
- **Progress bar** during document indexing
- **Document stats** — pages, chunks, word count

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS (cosine similarity) |
| LLM | OpenAI GPT-4o-mini |
| PDF Parsing | PyMuPDF |
| Language | Python |

## 📁 Project Structure

```
fin-report-analyzer/
├── app/
│   ├── app.py              ← Streamlit frontend
│   ├── ingest.py           ← PDF/TXT text extraction
│   ├── chunk.py            ← Overlapping text chunking
│   ├── embed_index.py      ← Embeddings + FAISS indexing
│   ├── retrieve.py         ← Semantic retrieval with confidence scores
│   ├── generate.py         ← LLM answer, summary, sentiment generation
│   └── prompts.py          ← Prompt templates
├── requirements.txt
└── README.md
```

## 🔧 Local Setup

```bash
# Clone the repo
git clone https://github.com/Krithikap019/fin-report-analyzer.git
cd fin-report-analyzer

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI key
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "your-key-here"' > .streamlit/secrets.toml

# Run the app
streamlit run app/app.py
```

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key (required for answer generation) |

## 💡 Why This Is Not Just "Using ChatGPT"

This system does not blindly feed the full document into an LLM. Instead it:
- Builds a **semantic index** of the document
- Retrieves only the **most relevant sections** per query
- **Grounds responses** in retrieved context only
- **Controls hallucination risk** with strict prompting
- Scales to **large documents** cost-efficiently

## 📈 What It Demonstrates

- NLP pipeline design
- Embedding-based semantic search
- Vector database integration (FAISS)
- LLM integration via API
- Prompt engineering
- Conversation memory management
- End-to-end system implementation