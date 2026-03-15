# AI Financial Report Analyzer

An AI-powered **Financial Report Analyzer** that ingests financial documents such as **10-K filings and earnings transcripts**, converts them into semantic embeddings, indexes them with **FAISS**, and answers natural-language questions using a **Retrieval-Augmented Generation (RAG)** pipeline.

The system allows users to upload financial reports and interact with them through natural language queries while showing the relevant evidence used to generate the answer.

---

# Features

- Upload **PDF or TXT financial reports**
- Extract text from financial documents
- Split documents into **semantic chunks**
- Generate embeddings using **SentenceTransformers**
- Store and search vectors using **FAISS**
- Ask **natural-language questions**
- Generate grounded answers using **OpenAI**
- Display retrieved evidence for transparency

---

# Tech Stack

- **Python**
- **Streamlit** – user interface
- **PyMuPDF** – PDF text extraction
- **SentenceTransformers** – text embeddings
- **FAISS** – vector similarity search
- **OpenAI API** – answer generation

---

# Project Structure

```bash
fin-report-analyzer/
│
├── app/
│   ├── frontend.py        # Streamlit interface
│   ├── ingest.py          # PDF/TXT text extraction
│   ├── chunk.py           # Document chunking
│   ├── embed_index.py     # Embedding generation + FAISS index
│   ├── retrieve.py        # Semantic search
│   ├── prompts.py         # Prompt templates
│   └── generate.py        # LLM answer generation
│
├── docs/                  # Sample financial documents
├── models/                # Cached embeddings / indexes
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Financial-Report-Analyzer.git
cd AI-Financial-Report-Analyzer
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate the Virtual Environment

### Mac / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pymupdf sentence-transformers faiss-cpu numpy openai
```

---

## 5. Set Your OpenAI API Key

### Mac / Linux

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Windows PowerShell

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

Restart the terminal if necessary.

---

## 6. Run the Application

```bash
streamlit run app/frontend.py
```

---

## 7. Open the App

Streamlit will usually open automatically. If not, go to:

```
http://localhost:8501
```

---

# How to Use

1. Upload a **PDF or TXT financial report**
2. Click **Index Document**
3. Enter a question about the report
4. View the generated answer and supporting evidence

---

# Example Questions

- What was total revenue for fiscal year 2024?
- What was the year-over-year revenue growth?
- What are the main risk factors mentioned?
- What was the net income in 2024?
- What business segments does the company operate in?
- What was operating cash flow?

---

# How It Works

The application follows a **Retrieval-Augmented Generation (RAG)** architecture.

### 1. Document Ingestion
Financial reports are uploaded and text is extracted from PDF or TXT files.

### 2. Chunking
Documents are split into overlapping chunks to preserve context.

### 3. Embedding Generation
Each chunk is converted into a semantic vector using a **SentenceTransformer model**.

### 4. Vector Indexing
Embeddings are stored in a **FAISS vector database** for fast similarity search.

### 5. Retrieval
When a user asks a question, the system retrieves the most relevant chunks using vector similarity.

### 6. Answer Generation
The retrieved chunks are passed to an **LLM (OpenAI)** which generates a grounded response using the document context.

---

# Example Architecture

```
Financial Document
       ↓
Text Extraction
       ↓
Chunking
       ↓
Embeddings (SentenceTransformers)
       ↓
Vector Index (FAISS)
       ↓
User Question
       ↓
Semantic Retrieval
       ↓
LLM Answer Generation
```

---

# Notes

- If the **OPENAI_API_KEY** is not set, the system can still retrieve relevant document sections but will not generate LLM answers.
- Large financial documents may take longer to index.
- If `faiss-cpu` installation fails, use Python **3.10 or 3.11**.

---

# Future Improvements

- Multi-document comparison
- Improved citation formatting
- Financial KPI extraction
- Complaint/theme clustering
- Interactive dashboards
- Deployment to **Hugging Face Spaces** or **Streamlit Cloud**

---

# License

This project is intended for **educational and portfolio use**.
