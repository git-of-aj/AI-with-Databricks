[Goat Real World problems of RAG](https://arpitbhayani.me/blogs/rag-production/)
- RAG with [azure ai search](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview?tabs=videos)

## GPT
Given your background (**Python + SQL databases**), I'd actually recommend this learning path:

```text
SQL Tables
    ↓
Embeddings
    ↓
ChromaDB (learning)
    ↓
Qdrant (production vector DB)
    ↓
PostgreSQL + pgvector
    ↓
Hybrid Search / RAG
    ↓
Production Architecture
```

The goal should be to **understand vectors**, not just learn a specific database.

# Phase 1 — Understand What a Vector Database Actually Stores

Most beginners imagine:

```sql
SELECT * FROM users;
```

A vector database is more like:

| id | text               | embedding                |
| -- | ------------------ | ------------------------ |
| 1  | "Cats are animals" | [0.12, -0.33, 0.77, ...] |
| 2  | "Dogs are pets"    | [0.08, -0.29, 0.81, ...] |

The embedding is simply a list of floating-point numbers:

```python
[0.12, -0.33, 0.77, 0.22, ...]
```

Modern models generate:

* 384 dimensions
* 768 dimensions
* 1024 dimensions
* 1536 dimensions
* 3072 dimensions

depending on the embedding model.

---

# Phase 2 — Create Embeddings Yourself

Create a project:

```bash
mkdir vector-learning
cd vector-learning

python -m venv venv
venv\Scripts\activate
```

Install:

```bash
pip install sentence-transformers
```

Create:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Cats are animals"

embedding = model.encode(text)

print(len(embedding))
print(embedding[:10])
```

Run:

```bash
python app.py
```

You will see:

```text
384
[0.021, -0.118, ...]
```

This is the most important moment.

You have created your first vector.

---

# Phase 3 — Learn Similarity Without Any Database

Create:

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = [
    "Cats are animals",
    "Dogs are pets",
    "Python is a programming language"
]

embeddings = model.encode(docs)

query = "Tell me about cats"

query_embedding = model.encode([query])

scores = cosine_similarity(
    query_embedding,
    embeddings
)

print(scores)
```

You should see the cat sentence score highest.

This is literally what every vector database does internally.

---

# Phase 4 — Install ChromaDB

Install:

```bash
pip install chromadb
```

Create:

```python
import chromadb

client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="animals"
)
```

---

# Insert Data

```python
collection.add(
    documents=[
        "Cats are animals",
        "Dogs are pets",
        "Python is a programming language"
    ],
    ids=["1","2","3"]
)
```

---

# SQL Equivalent

SQL:

```sql
SELECT * FROM animals;
```

Chroma:

```python
results = collection.get()

print(results)
```

You can see:

```python
{
 'ids': [...],
 'documents': [...]
}
```

---

# Filter Like SQL WHERE

SQL:

```sql
SELECT *
FROM animals
WHERE category='pet';
```

Chroma:

```python
collection.add(
    documents=["Dogs are pets"],
    ids=["4"],
    metadatas=[
        {"category":"pet"}
    ]
)
```

Query:

```python
collection.get(
    where={
        "category":"pet"
    }
)
```

---

# Similarity Search

SQL mindset:

```sql
SELECT *
ORDER BY similarity DESC;
```

Chroma:

```python
collection.query(
    query_texts=[
        "Tell me about dogs"
    ],
    n_results=3
)
```

This is the equivalent of:

```sql
TOP 3 nearest neighbors
```

---

# Phase 5 — Actually Look At Stored Embeddings

Most beginners miss this.

Store your own embeddings:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embedding = model.encode(
    "Cats are animals"
).tolist()

print(embedding)
```

Insert:

```python
collection.add(
    ids=["1"],
    embeddings=[embedding],
    documents=["Cats are animals"]
)
```

Retrieve:

```python
collection.get(
    include=["embeddings"]
)
```

Now you can literally inspect the vectors.

---

# Phase 6 — Learn Qdrant

Install:

```bash
pip install qdrant-client
```

Run locally:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

(or use Qdrant Cloud)

Create collection:

```python
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333
)

client.create_collection(
    collection_name="animals",
    vectors_config={
        "size":384,
        "distance":"Cosine"
    }
)
```

---

Insert vectors:

```python
client.upsert(
    collection_name="animals",
    points=[
        {
            "id":1,
            "vector":embedding.tolist(),
            "payload":{
                "text":"Cats are animals"
            }
        }
    ]
)
```

Retrieve:

```python
client.scroll(
    collection_name="animals"
)
```

This feels very similar to:

```sql
SELECT *
FROM animals;
```

---

# Phase 7 — Learn pgvector

Install PostgreSQL.

Enable extension:

```sql
CREATE EXTENSION vector;
```

Create table:

```sql
CREATE TABLE documents
(
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(384)
);
```

Insert:

```sql
INSERT INTO documents
(
    content,
    embedding
)
VALUES
(
    'Cats are animals',
    '[0.1,0.2,0.3,...]'
);
```

---

View vectors:

```sql
SELECT *
FROM documents;
```

This is why SQL developers love pgvector.

You can literally see embeddings in rows.

---

Similarity search:

```sql
SELECT *
FROM documents
ORDER BY embedding <=> '[0.2,0.4,...]'
LIMIT 5;
```

Where:

```text
<=> = cosine distance
```

This feels almost exactly like SQL.

---

# Final Learning Roadmap (2 Weeks)

### Days 1–2

Learn:

* Embeddings
* Cosine similarity
* Sentence Transformers

Build:

```text
Python only
No database
```

---

### Days 3–4

Learn:

* ChromaDB

Practice:

```python
add()
get()
delete()
query()
```

Look at actual stored vectors.

---

### Days 5–7

Learn:

* Qdrant

Practice:

* collections
* payloads
* filtering
* similarity search

---

### Days 8–10

Learn:

* PostgreSQL + pgvector

Practice:

```sql
SELECT
INSERT
WHERE
ORDER BY embedding <=> vector
```

---

### Days 11–14

Build a mini RAG system:

```text
PDF
 ↓
Chunking
 ↓
Embeddings
 ↓
Qdrant / pgvector
 ↓
Similarity Search
 ↓
LLM
```

-------------------

### Real World Probs

#### Chunking
- chunks need to be small enough that retrieved text is specific and relevant, but large enough that they contain complete thoughts. In practice, getting this right requires understanding your document corpus.
- Always store metadata with each chunk: the source document ID, section heading, page number, creation timestamp, and a content hash. You will need all of these later, both for filtering and for keeping the index current.
-  15 chunks produces 15 separate vectors, each stored with its own ID. When that document is updated, you cannot simply update a row as you would in a relational database. You need to:

1. Identify all 15 chunk IDs that belong to the old version of the document
2. Delete them from the vector store
3. Re-chunk the updated document (which may now produce 17 chunks)
4. Re-embed and insert the 17 new chunks
This requires a mapping layer that vector databases do not provide natively. The standard approach is a document registry, a simple relational table (Postgres works fine) that maps each doc_id to the list of chunk vector IDs currently in the index:
```sql
CREATE TABLE doc_chunk_registry (
    doc_id          TEXT NOT NULL,
    chunk_vector_id TEXT NOT NULL,
    content_hash    TEXT NOT NULL,
    version         INTEGER NOT NULL DEFAULT 1,
    indexed_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status          TEXT NOT NULL DEFAULT 'active',  -- 'active' | 'deleted' | 'superseded'
    PRIMARY KEY (doc_id, chunk_vector_id)
);
```
- **Re-Embed Onlyy whats change not everything as a dumbass.. thats why use content hash**
#### Vectors
- Every vector in your index was produced by that model. If you switch models, every vector is now incommensurable with the new query embeddings, and you must re-embed the entire corpus.
#### Indexing Pipeline
- Your knowledge base is not static. Documents are updated, retracted, corrected, superseded, and deleted. If your indexing pipeline cannot handle these operations correctly, your RAG system will quietly serve stale, contradictory, or deleted information with full confidence.
- ou start reindexing 10,000 documents, the pipeline crashes at document 6,000, some documents are at version N, some at version N+1, and the seam between them is invisible to the retrieval layer.
```sql
rag_index_2026_05_14  (built overnight, fully validated)
rag_index_current     (alias pointing to above)
```
- You build the new index completely, validate it against a benchmark query set, then atomically swap the alias. The old index stays around for a configurable retention period in case rollback is needed. No query ever sees a partial index
### But My App gives Wrong or Suboptimal answers?
> might be a false positive from an embedding space where the query and an unrelated chunk happen to land nearby.
- After reranking, send the top-5 chunks and the query to the LLM with a short system prompt asking it to explain the relevance of each chunk before generating the final answer. The rationale is logged as a structured field on the trace. This is expensive if done per-request, but extremely valuable when run on a sampled basis (say, 1% of production traffic plus 100% of user-flagged responses)
- **Retrieval vs answer Quality**:after the main LLM generates an answer, send the answer, the retrieved context, and the original question to a smaller, cheaper model with a rubric asking it to score faithfulness (did the answer stay within what the context says?) and relevance (did the answer address the question?). Log these scores alongside the trace ID.
1. Retrieved chunks are from the wrong document (index corruption or model drift)
2. Retrieved chunks are from the right document but the wrong section (chunking boundary problem)
3. Retrieved chunks are correct but the LLM ignored them (a generation problem, not a retrieval problem)
