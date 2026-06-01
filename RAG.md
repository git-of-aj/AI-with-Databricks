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

If your goal is to become production-ready, I would spend **only 2–3 days on ChromaDB**, then move quickly to **Qdrant** and **pgvector**, because those are the technologies you're most likely to encounter in real production systems today.
