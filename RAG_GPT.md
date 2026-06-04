You're asking the right question. A production RAG system is **not just embeddings + vector DB**. The hardest engineering problem is actually **incremental indexing and synchronization**.

After reviewing Azure documentation, LlamaIndex ingestion docs, and engineering discussions around production RAG systems, here's the architecture I'd recommend. ([Developer Documentation][1])

---

# First: Correct Mental Model

Many engineers think:

```text
Documents
   ↓
Chunk
   ↓
Embed
   ↓
Vector DB
   ↓
LLM
```

In production, it looks more like:

```text
Documents
   ↓
Change Detection
   ↓
Parsing
   ↓
Chunking
   ↓
Chunk Hashing
   ↓
Embedding
   ↓
Vector DB
   ↓
Retriever
   ↓
LLM
```

The **Retriever** sits between the LLM and vector DB.

So the answer to your second question:

> Does LLM connect directly to vector DB?

Generally **No**.

Instead:

```text
User Query
     ↓
Retriever
     ↓
Vector DB
     ↓
Top-K Chunks
     ↓
Prompt Builder
     ↓
LLM
     ↓
Answer
```

The LLM never talks to the vector DB directly.

A typical production query flow:

```python
question
   -> embedding(question)
   -> vector search
   -> retrieve chunks
   -> rerank
   -> build prompt
   -> send to LLM
```

---

# Production RAG Indexing Pipeline

The biggest mistake people make:

```text
File changed
   ↓
Delete all vectors
   ↓
Re-embed everything
```

This becomes extremely expensive.

Instead use:

```text
Document Hash
      +
Chunk Hash
```

to identify exactly what changed.

This is the same philosophy used by LlamaIndex's document management pipeline, which stores document hashes and only reprocesses changed content. ([Developer Documentation][1])

---

# Metadata You Should Store

For every chunk:

```json
{
  "chunk_id": "uuid",
  "document_id": "employee_handbook_v1",
  "chunk_hash": "sha256(...)",
  "embedding_model": "bge-large-en-v1.5",
  "chunk_text": "...",
  "created_at": "...",
  "updated_at": "..."
}
```

---

# Incremental Update Algorithm

## Step 1: Detect File Changes

Watch:

```text
pdf
txt
md
docx
html
```

using:

### Local

```python
watchdog
```

or

```python
watchfiles
```

---

Example:

```python
watchdog.Observer()
```

Events:

```text
CREATED
MODIFIED
DELETED
```

---

# Step 2: Parse Document

Use:

```text
Unstructured
LlamaParse
PyMuPDF
Markdown parser
```

Extract raw text.

---

# Step 3: Chunk

Example:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
```

Store:

```python
document_id
chunk_index
chunk_text
```

---

# Step 4: Hash Each Chunk

```python
hashlib.sha256(chunk_text.encode())
```

Example:

```python
chunk_hash
```

Store hashes in:

```text
SQLite
Postgres
DuckDB
```

---

# Step 5: Compare Old vs New

Suppose:

Old:

```text
Chunk A
Chunk B
Chunk C
Chunk D
```

New:

```text
Chunk A
Chunk B modified
Chunk C
Chunk E
```

Hash comparison shows:

```text
A unchanged
B modified
C unchanged
D deleted
E added
```

Result:

```text
Re-embed B
Embed E
Delete D
```

Only 2 chunks processed.

Not entire document.

This is exactly the pattern discussed in incremental ingestion frameworks and production RAG systems. ([Developer Documentation][1])

---

# CRUD Operations on Vector DB

## CREATE

```python
vector_db.upsert(new_chunk)
```

---

## UPDATE

Most vector DBs support:

```python
upsert(id)
```

which means:

```text
if exists -> update
else -> insert
```

---

## DELETE

```python
vector_db.delete(
   filter={"document_id": doc_id}
)
```

or

```python
vector_db.delete(chunk_id)
```

---

# Local Open Source Stack (Recommended)

If I were building today:

### Parsing

```text
Unstructured
PyMuPDF
markdown-it-py
```

---

### Chunking

```text
LlamaIndex
LangChain text splitters
```

---

### Embeddings

```text
BAAI/bge-large-en-v1.5
bge-m3
nomic-embed-text
```

Run locally:

```text
Ollama
vLLM
TEI
```

---

### Vector DB

For local production:

```text
Qdrant
```

Best balance of:

```text
performance
filtering
ease of operation
```

Alternatives:

```text
Weaviate
Milvus
Chroma
```

---

### Metadata Store

```text
Postgres
```

Store:

```text
documents
chunks
hashes
versions
```

Do NOT rely on vector DB as your source of truth.

---

### File Monitoring

```text
watchdog
watchfiles
```

---

### Workflow Orchestration

```text
Temporal
Prefect
Dagster
```

For serious production systems.

---

# Recommended Local Architecture

```text
Filesystem
      ↓
Watchdog
      ↓
Parser
      ↓
Chunker
      ↓
Hash Calculator
      ↓
Diff Engine
      ↓
Embedding Service
      ↓
Qdrant
```

Metadata:

```text
Postgres
```

---

# Azure Production Architecture

This is what most enterprises end up using.

```text
Azure Blob Storage
        ↓
Azure Event Grid
        ↓
Azure Function
        ↓
Chunking Service
        ↓
Azure OpenAI Embeddings
        ↓
Azure AI Search Vector Index
```

---

## Service Mapping

### File Storage

Use:

Azure Blob Storage

Store:

```text
pdf
docx
md
txt
```

---

### Detect Changes

Use:

Azure Event Grid

Triggers:

```text
BlobCreated
BlobDeleted
BlobModified
```

No polling needed.

---

### Processing

Use:

Azure Functions

Handles:

```text
parse
chunk
hash
embed
upsert
```

---

### Metadata Database

Use:

Azure Database for PostgreSQL

Store:

```text
document hashes
chunk hashes
versions
```

---

### Embeddings

Use:

Azure OpenAI Service

Example:

```text
text-embedding-3-large
text-embedding-3-small
```

---

### Vector Storage

Two good options:

#### Option A (My recommendation)

Azure AI Search

Provides:

```text
Vector Search
Hybrid Search
Semantic Search
Filters
Chunking
Integrated Vectorization
```

Also supports incremental indexing and change detection for Blob Storage. ([Microsoft Learn][2])

---

#### Option B

Self-hosted:

```text
Qdrant on AKS
Milvus on AKS
```

when you need:

```text
100M+ vectors
advanced retrieval
lower cost
```

---

# Azure Native Incremental Indexing

Azure AI Search can automatically detect:

```text
new files
updated files
```

using blob timestamps and incremental indexing. ([Microsoft Learn][2])

Deletion handling requires configuring a deletion strategy (soft delete metadata or blob soft delete). ([Microsoft Learn][3])

However, if you want **chunk-level re-embedding only**, I would still build a custom pipeline with chunk hashes rather than relying entirely on the built-in indexer.

---

# Architecture I'd Use Today

## Local

```text
Watchdog
    ↓
Unstructured
    ↓
LlamaIndex Ingestion
    ↓
Chunk Hashing
    ↓
BGE-M3
    ↓
Qdrant
    ↓
Retriever
    ↓
LLM
```

---

## Azure Enterprise

```text
Blob Storage
      ↓
Event Grid
      ↓
Azure Functions
      ↓
Chunk Hashing
      ↓
Azure OpenAI Embeddings
      ↓
Azure AI Search
      ↓
Retriever API
      ↓
GPT-4.1 / GPT-4o
```

---

One additional production recommendation: **separate chunking from embedding**. Store chunk text and hashes permanently. If you later switch embedding models, you can regenerate vectors from stored chunks without re-parsing all documents. Engineers who tightly couple chunking and embedding often end up reprocessing millions of documents when changing embedding models. ([Reddit][4])

[1]: https://docs.llamaindex.ai/en/v0.10.33/examples/ingestion/document_management_pipeline/?utm_source=chatgpt.com "Ingestion Pipeline + Document Management - LlamaIndex"
[2]: https://learn.microsoft.com/en-us/azure/search/search-howto-indexing-azure-blob-storage?utm_source=chatgpt.com "Azure blob indexer - Azure AI Search | Microsoft Learn"
[3]: https://learn.microsoft.com/en-us/azure///search/search-howto-index-changed-deleted-blobs?utm_source=chatgpt.com "Changed and deleted blobs - Azure AI Search | Microsoft Learn"
[4]: https://www.reddit.com/r/Rag/comments/1rqw1oo/i_had_to_reembed_5_million_documents_because_i/?utm_source=chatgpt.com "I had to re-embed 5 million documents because I changed embedding models. Here's how to never be in that position."
