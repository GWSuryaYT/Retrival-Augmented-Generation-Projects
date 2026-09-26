# Version 2 RAG

Another Python-based Retrieval-Augmented Generation (RAG) pipeline that processes text documents, generates vector embeddings using Google Gemini, stores them in ChromaDB, and retrieves relevant context to answer user queries.

---

## File Overview

| File | Description |
| --- | --- |
| `chunker.py` | Contains the `Chunky` class for splitting text into word-bounded chunks based on full stops with customizable word overlap.

 |
| `databases.py` | Defines the `Vector_Storage` class that handles text embedding via Gemini (`gemini-embedding-2`) and database operations in ChromaDB.

 |
| `rag_pipeline.py` | Execution script that checks vector storage, populates missing embeddings, queries the vector database, and passes context to Gemini (`gemini-3.1-flash-lite`).

 |

---

## Key Features

* **Custom Sentence-Based Chunker**: Splits raw paragraphs on period (`.`) boundaries while respecting target word counts (`chunk_size`) and preserving semantic context using trailing word overlap (`overlap`).


* **Persistent Vector Store**: Uses ChromaDB (`PersistentClient` stored at `./my_vector_database`) under collection name `vector_storage` to preserve embedded data.


* **Gemini Embeddings**: Encodes document chunks into vector format using Google GenAI's `gemini-embedding-2` model.


* **Contextual Answer Generation**: Leverages `gemini-3.1-flash-lite` via `google.genai` SDK interactions to generate answers grounded in retrieved database context.



---

## Prerequisites & Installation

1. **Python Version**: Python 3.8+
2. **Install Required Packages**:
```bash
pip install chromadb google-genai python-dotenv

```



---

## Configuration

Set your Google Gemini API key in a `.env` file in your root project directory:

```env
GEMINI_KEY=your_gemini_api_key_here

```

---

## System Architecture & API Details

### 1. Text Chunking (`chunker.py`)

```python
from chunker import Chunky

chunker = Chunky()
chunks = chunker.chunk_maker(paragraph="Your text here...", overlap=10, chunk_size=30)

```

* **`paragraph`** *(str)*: Text block to split.


* **`chunk_size`** *(int, default=30)*: Maximum word count threshold before initiating a chunk split.


* **`overlap`** *(int, default=10)*: Number of trailing words carried over to the start of the subsequent chunk.



### 2. Vector Operations (`databases.py`)

```python
from databases import Vector_Storage

vec_store = Vector_Storage()

# Generate vector embeddings
embedding_vector = vec_store.gemini_encodding(text="Sample text")

# Store document chunks into ChromaDB
vec_store.store(paragraph="Your text...", chunk_size=20, over_lap=10)

# Query vector similarity (returns top_k results)
results = vec_store.result(query_vector=embedding_vector, top_k=2)

```

---

## How to Run

Execute the main RAG pipeline script:

```bash
python rag_pipeline.py

```

### Execution Flow:

1. **Database Check**: Reads `./my_vector_database`. If the `vector_storage` collection count is 0, it chunks and embeds the source text.


2. **Query Processing**: Embeds the prompt (`"what to grow in garden?"`) using `gemini-embedding-2`.


3. **Similarity Search**: Queries ChromaDB for the top 2 matching context chunks.


4. **Response Generation**: Sends user input alongside matching document context to `gemini-3.1-flash-lite` to produce the final output.