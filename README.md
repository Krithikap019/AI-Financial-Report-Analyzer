AI-Financial-Report-Analyzer
/README.md

Preview

Code

Blame
160 lines (93 loc) · 3.25 KB
AI Financial Report Analyzer

An AI-powered Financial Report Analyzer that ingests financial documents such as 10-K filings and earnings transcripts, converts them into semantic embeddings, indexes them with FAISS, and answers natural-language questions using a Retrieval-Augmented Generation (RAG) pipeline.

Features

Upload PDF or TXT financial reports

Extract and chunk document text

Generate semantic embeddings using SentenceTransformers

Store and search embeddings with FAISS

Ask natural-language questions about the report

Generate grounded answers using OpenAI

Display retrieved evidence for transparency

Tech Stack

Python

Streamlit

PyMuPDF

SentenceTransformers

FAISS

OpenAI API

Project Structure fin-report-analyzer/ │ ├── app/ │ ├── frontend.py │ ├── ingest.py │ ├── chunk.py │ ├── embed_index.py │ ├── retrieve.py │ ├── prompts.py │ └── generate.py │ ├── docs/ ├── models/ ├── requirements.txt └── README.md

Setup Instructions

Clone the repository git clone https://github.com/your-username/fin-report-analyzer.git cd fin-report-analyzer

Create a virtual environment python -m venv venv

Activate the virtual environment Mac / Linux source venv/bin/activate

Windows venv\Scripts\activate

Install dependencies pip install -r requirements.txt
If you do not have a requirements.txt yet, install manually:

pip install streamlit pymupdf sentence-transformers faiss-cpu numpy openai

Set your OpenAI API key Mac / Linux export OPENAI_API_KEY="your_api_key_here"
Windows PowerShell setx OPENAI_API_KEY "your_api_key_here"

Then restart the terminal if needed.

Run the application streamlit run app/frontend.py

Open the app in your browser

Streamlit will usually open automatically. If not, go to:

http://localhost:8501

How to Use

Upload a PDF or TXT financial report

Click Index Document

Enter a question such as:

What was total revenue in 2024?

What was the YoY revenue growth?

What are the major risk factors?

How much was invested in R&D?

Review the generated answer and retrieved evidence

Example Questions

What was total revenue for fiscal year 2024?

What were the top 3 risk factors?

What was net income in 2024?

What were the business segments?

What was operating cash flow?

How It Works

Document ingestion: Extracts text from PDF or TXT files

Chunking: Splits the text into overlapping chunks

Embedding generation: Converts chunks into vector embeddings

FAISS indexing: Stores embeddings for similarity search

Retrieval: Finds the most relevant chunks for a user query

Answer generation: Uses OpenAI to generate a grounded response based on retrieved context

Notes

If OPENAI_API_KEY is not set, the app can still retrieve relevant evidence chunks, but answer generation will be limited.

Large PDFs may take longer to index depending on system resources.

FAISS installation may vary by environment. If faiss-cpu fails, try using a compatible Python version such as 3.10 or 3.11.

Future Improvements

Multi-document comparison

Better citation formatting

Complaint/theme clustering

Dashboard-style financial KPI extraction

Deployment to Hugging Face Spaces or Streamlit Cloud

License

This project is for educational and portfolio use.
