```markdown
# Gemini RAG Pipeline from Scratch

A lightweight, modular Retrieval-Augmented Generation (RAG) system built in Python from first principles. This repository implements custom text chunking, an in-memory vector store, manual cosine similarity calculations, and integration with Google's Gemini API for text embedding and context-constrained response generation.

---

## Features

- **Custom Text Chunking**: Sentence-aware paragraph splitting with adjustable chunk sizes and overlapping windows (`chunker.py`).
- **Manual Vector Math**: Pure Python implementation of cosine similarity for vector similarity scoring without heavy mathematical library dependencies (`vector_math.py`).
- **In-Memory Vector Store**: Simple database structure to store, rank, and retrieve text chunks based on semantic similarity (`vector_store.py`).
- **Gemini API Integration**: Uses `google-genai` to generate text embeddings via `gemini-embedding-2` and output responses via `gemini-3.1-flash-lite` (`embedding.py`, `rag_pipeline.py`).
- **Strict Context Prompting**: Prompts the LLM to answer user queries exclusively using retrieved context.

---

## File Structure

```text
.
├── api.py           # Loads environment variables and exposes GEMINI_API_KEY
├── chunker.py       # Custom sentence-based text chunking algorithm
├── embedding.py     # Interfaces with Gemini API to generate embeddings for text chunks
├── vector_math.py   # Pure Python cosine similarity calculation
├── vector_store.py  # In-memory vector database for storing and querying embeddings
└── rag_pipeline.py  # End-to-end execution script demonstrating the RAG workflow

```

---

## Prerequisites

* Python 3.9+
* A Google Gemini API key

---

## Installation & Setup

1. **Clone the repository**:
```bash
git clone [https://github.com/gwsuryayt/gemini-rag-from-scratch.git](https://github.com/gwsuryayt/gemini-rag-from-scratch.git)
cd gemini-rag-from-scratch

```


2. **Install dependencies**:
```bash
pip install google-genai python-dotenv

```


3. **Configure Environment Variables**:
Create a `.env` file in the root directory and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here

```



---

## How It Works

### 1. Text Chunking (`chunker.py`)

Splits large text paragraphs into smaller, overlapping segments based on full-stop sentence boundaries to preserve context across boundaries:

* `chunk_size`: Target word count per chunk.
* `over_lap`: Number of overlapping words retained from the end of the previous chunk.

### 2. Embeddings (`embedding.py`)

Sends chunked text blocks to the Gemini API (`gemini-embedding-2` model) to obtain dense vector representations.

### 3. Vector Similarity (`vector_math.py`)

Computes similarity between the user query vector ($\mathbf{A}$) and stored chunk vectors ($\mathbf{B}$) using the cosine similarity formula:

$$\text{Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\Vert{}\mathbf{A}\Vert{} \Vert{}\mathbf{B}\Vert{}} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

### 4. Vector Store (`vector_store.py`)

Maintains an in-memory list of document chunks and their associated vector embeddings. When queried, it scores all stored items against the query vector and returns the $Top\text{-}K$ most relevant matches.

### 5. RAG Execution (`rag_pipeline.py`)

Retrieves relevant text snippets using `VectorStore` and prompts `gemini-3.1-flash-lite` to answer user questions using **only** the retrieved context.

---

## Usage Example

To run the complete pipeline with the included example:

```bash
python rag_pipeline.py

```

### Code Example

```python
from vector_store import VectorStore
from google import genai
from api import api_giver

# Initialize API Client and Vector Store
ai_client = genai.Client(api_key=api_giver())
store = VectorStore()

# 1. Add document text to the vector store
sample_text = "Gardening is a wonderful hobby. It brings people closer to nature..."
store.add_chunks(paragraph=sample_text, chunk_size=30, over_lap=15)

# 2. Query top relevant context
query = "Tell me about gardening benefits."
results = store.search(query_text=query, top_k=2)
context = "\n".join([item["text"] for item in results])

# 3. Generate response with constrained context
response = ai_client.interactions.create(
    model="gemini-3.1-flash-lite",
    input=f"Answer using ONLY this context:\n{context}\n\nQuestion: {query}"
)

print(response.output_text)

```

```

```