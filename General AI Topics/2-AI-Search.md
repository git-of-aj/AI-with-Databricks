## My data
Azure AI search:
- Indexing loads content into an index and makes it searchable.
- You can use the push method to upload JSON documents directly or the pull method (indexer or logic app workflow) to retrieve and serialize data into JSON.
- targets an index populated with searchable content. This step occurs when your client app sends a query request to your search service

[what is index](https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index)
- a search index equates to a table, and documents are roughly equivalent to rows in a table.
- An index is continuously available and can't be paused or taken offline. Because it's designed for continuous operation, updates to its content and additions to the index itself happen in real time. If a request coincides with a document update, queries might temporarily return incomplete results.

[Indexer - ms docs](https://learn.microsoft.com/en-us/azure/search/search-indexer-overview)
- An indexer in Azure AI Search is a crawler that extracts textual data from cloud data sources and populates a search index using field-to-field mappings between source data and a search index. This approach is sometimes referred to as a 'pull model' because the search service pulls data in without you having to write any code that adds data to an index.

1. Step 1: Create a data source (Pass creds)
2. Step 2: Create an index (map input and output fields via  define field mappings )
3. Step 3: Create and run (or schedule) the indexer

> On subsequent runs, the indexer can usually detect and retrieve just the data that has changed. For blob data, change detection is automatic. For other data sources like Azure SQL or Azure Cosmos DB, change detection must be enabled.
# GPT
I read the two Microsoft Learn articles and related Azure AI Search documentation. Here's the practical explanation.

**Sources:**

* Search Index: [Search Index Overview](https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index?utm_source=chatgpt.com)
* Vector Store: [Vector Store in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/vector-store?utm_source=chatgpt.com)
* Vector Index Creation: ([Microsoft Learn][1])
* Azure AI Search Overview: ([Microsoft Learn][2])

---

# 1. What problem does a Search Index solve?

A **search index** is Azure AI Search's core data structure that stores your searchable documents. It is optimized for:

* Keyword search
* Full-text search
* Filters
* Sorting
* Facets
* Autocomplete
* Hybrid search
* Vector search (if vector fields exist)

Think of it as:

> "A database specifically designed for search."

Instead of querying PDFs directly from Blob Storage every time, Azure creates an index containing searchable representations of your data. Queries hit the index, not the original PDFs. ([Microsoft Learn][3])

Example:

PDF contains:

> Azure OpenAI supports GPT-4o.

Search index stores searchable fields:

```json
{
  "id": "1",
  "title": "Azure OpenAI Guide",
  "content": "Azure OpenAI supports GPT-4o..."
}
```

Now searches are milliseconds instead of scanning PDFs every query. ([Microsoft Learn][3])

---

# 2. What problem does a Vector Store solve?

A **vector store** solves semantic search.

Keyword search fails when words differ.

Example:

Document says:

> "Annual leave policy"

User asks:

> "How many vacation days do employees get?"

Keyword search may miss it.

Vector search converts both document and question into embeddings (vectors) and finds semantic similarity rather than exact words. ([Microsoft Learn][1])

Vector store enables:

* Semantic search
* Similarity search
* RAG retrieval
* AI assistants
* Chatbots

Example:

```text
Document:
"Employees receive 20 annual leave days."

Question:
"How many vacation days do I get?"
```

Different words.

Similar meaning.

Vector search retrieves it. ([Microsoft Learn][1])

---

# 3. Important misconception

Many people think:

```text
Search Index
and
Vector Index
```

are two separate Azure resources.

Not really.

In Azure AI Search:

**Vector data lives inside a search index.**

A vector index is simply:

```text
Search Index
+
Vector Fields
+
Vector Configuration
```

Microsoft explicitly defines a vector index as a search index containing vector fields and vector search configuration. ([Microsoft Learn][1])

---

# 4. What do they have in common?

Both require almost identical setup.

## A. Schema first

Before loading data, you define fields.

Example:

```json
{
  "name": "content",
  "type": "Edm.String"
}
```

or

```json
{
  "name": "contentVector",
  "type": "Collection(Edm.Single)"
}
```

Schema is created first, data loaded second. ([Microsoft Learn][4])

---

## B. Both use an Azure AI Search Index

Both live inside the same search service.

```text
Azure AI Search
 └── Index
      ├── text fields
      ├── metadata fields
      └── vector fields
```

([Microsoft Learn][3])

---

## C. Both can use Indexers

You can ingest data using:

### Push model

Your code uploads documents.

or

### Pull model (Indexer)

Azure AI Search indexer reads Blob Storage and populates the index automatically. ([Microsoft Learn][5])

---

## D. Both can use AI enrichment

Indexers can:

* OCR
* Chunk text
* Generate embeddings
* Extract metadata

before writing to the index. ([Microsoft Learn][5])

---

## E. Both are queried through the same endpoint

```text
/indexes/my-index/docs/search
```

Difference is only the query type. ([Microsoft Learn][6])

---

# 5. What is different?

| Feature             | Search Index     | Vector Store        |
| ------------------- | ---------------- | ------------------- |
| Search method       | Keyword matching | Semantic similarity |
| Data stored         | Text fields      | Embedding vectors   |
| Query type          | Full text search | Vector search       |
| Finds exact words   | Excellent        | Not primary purpose |
| Finds meaning       | Limited          | Excellent           |
| RAG usage           | Useful           | Essential           |
| Embeddings needed   | No               | Yes                 |
| Uses LLM embeddings | No               | Yes                 |

---

# 6. Real-world PDF example

Suppose you have:

```text
Blob Storage
 ├── HR.pdf
 ├── LeavePolicy.pdf
 ├── TravelPolicy.pdf
 └── BenefitsGuide.pdf
```

Goal:

```text
Chatbot answers questions from PDFs
```

---

# Option 1: Traditional Search Index

## Step 1

Create Azure AI Search service.

---

## Step 2

Create Blob Storage datasource.

```text
Data Source
    -> Blob Container
```

---

## Step 3

Create Search Index.

Schema:

```json
{
  "id": "...",
  "title": "...",
  "content": "..."
}
```

---

## Step 4

Create Indexer.

```text
Blob Storage
      ↓
Indexer
      ↓
Search Index
```

Indexer extracts text from PDFs. ([Microsoft Learn][5])

---

## Step 5

Query

```text
search=vacation policy
```

Returns matching documents.

Problem:

```text
vacation ≠ annual leave
```

Results may be poor.

---

# Option 2: Vector Store for RAG

This is what most modern AI apps use.

---

## Step 1

Create Azure AI Search service.

---

## Step 2

Create datasource to Blob Storage.

---

## Step 3

Chunk PDFs

Example:

```text
Leave Policy PDF

Chunk 1
Chunk 2
Chunk 3
Chunk 4
```

Rather than storing whole PDF as one document.

Azure AI enrichment can do chunking automatically. ([Microsoft Learn][5])

---

## Step 4

Generate embeddings

Each chunk becomes:

```text
Chunk text
      ↓
Embedding Model
      ↓
1536-dimensional vector
```

Example model:

```text
text-embedding-3-small
```

from Azure OpenAI.

---

## Step 5

Create Vector Index

Schema:

```json
{
  "chunkId": "...",
  "content": "...",
  "contentVector": [0.12, 0.98, ...]
}
```

Vector field:

```json
"contentVector"
```

stores embeddings. ([Microsoft Learn][1])

---

## Step 6

Run Indexer

```text
Blob PDFs
     ↓
Chunking
     ↓
Embedding generation
     ↓
Vector Index
```

Modern Azure AI Search can do this through integrated vectorization. ([Microsoft Learn][1])

---

# Building the RAG App

Now user asks:

```text
How many vacation days do employees receive?
```

---

## Retrieval phase

Question

```text
How many vacation days...
```

↓

Embedding Model

↓

Query Vector

↓

Azure AI Search Vector Search

↓

Top matching chunks

Example:

```text
Chunk 17:
Employees receive 20 annual leave days.
```

([Microsoft Learn][1])

---

## Generation phase

Prompt sent to GPT:

```text
Context:

Employees receive 20 annual leave days.

Question:

How many vacation days do employees receive?
```

GPT responds:

```text
Employees receive 20 annual leave days per year.
```

---

# What most production RAG systems actually use

They don't choose one or the other.

They use:

```text
Hybrid Search
```

which combines:

```text
Keyword Search
+
Vector Search
```

inside the same Azure AI Search index. Azure AI Search explicitly supports hybrid retrieval and recommends it for many RAG scenarios. ([Microsoft Learn][2])

Architecture:

```text
Blob PDFs
     ↓
Indexer
     ↓
Chunking
     ↓
Embeddings
     ↓
Azure AI Search Index
       ├── content (text)
       └── contentVector (vector)
     ↓
Hybrid Search
     ↓
Top Chunks
     ↓
Azure OpenAI
     ↓
Answer
```

If you're building a RAG chatbot over PDFs today, the recommended design is **one Azure AI Search index containing both text fields and vector fields**, populated via an indexer + chunking + embeddings pipeline, then queried using **hybrid search** before sending retrieved chunks to Azure OpenAI. ([Microsoft Learn][2])

[1]: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-create-index?utm_source=chatgpt.com "Create a Vector Index - Azure AI Search | Microsoft Learn"
[2]: https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search?utm_source=chatgpt.com "Introduction to Azure AI Search - Azure AI Search | Microsoft Learn"
[3]: https://learn.microsoft.com/en-gb/azure/search/search-what-is-an-index?utm_source=chatgpt.com "Search index overview - Azure AI Search | Microsoft Learn"
[4]: https://learn.microsoft.com/en-us/azure/search/search-how-to-create-search-index?utm_source=chatgpt.com "Create a Search Index - Azure AI Search | Microsoft Learn"

---
Yes, that's a good mental model, with one important nuance.

You can roughly think of:

```text
Traditional Search Index
≈ BM25-based retrieval
```

because Azure AI Search's full-text search engine uses variants of the classic inverted-index approach and ranks keyword matches using **BM25** by default.

So:

| Concept      | What it does                                     |
| ------------ | ------------------------------------------------ |
| Search Index | Stores searchable text in an inverted index      |
| BM25         | Ranking algorithm used on that index             |
| Query        | Matches keywords and ranks results by BM25 score |

Example:

Document A:

> Employees receive 20 annual leave days.

Document B:

> Employees receive health insurance benefits.

Query:

```text
annual leave
```

BM25 scores Document A higher because it contains both terms and they are relatively distinctive.

---

### More precise wording

Instead of saying:

> Search Index solves BM25 search

I'd say:

> A Search Index enables keyword-based information retrieval, typically using an inverted index and BM25 ranking.

or

> Azure AI Search's traditional retrieval mode is BM25-based search over a search index.

---

### Relationship to Vector Search

A useful comparison:

| Traditional Search Index            | Vector Search                           |
| ----------------------------------- | --------------------------------------- |
| Inverted index                      | Vector index (HNSW, ANN)                |
| BM25 ranking                        | Cosine similarity / vector similarity   |
| Exact words matter                  | Meaning matters                         |
| "annual leave" finds "annual leave" | "vacation days" can find "annual leave" |
| Fast keyword retrieval              | Semantic retrieval                      |
| Search engines                      | RAG systems, chatbots                   |

---

### In a modern RAG pipeline

You usually have **both** inside the same Azure AI Search index:

```text
PDF
 ↓
Chunking
 ↓
Azure AI Search Index
 ├── content             (BM25 search)
 └── contentVector       (Vector search)
```

When a user asks:

```text
How many vacation days do employees get?
```

Azure can perform:

```text
BM25 Search
+
Vector Search
=
Hybrid Search
```

and then merge/rerank the results.

This hybrid approach is what Microsoft generally recommends for RAG because BM25 and vector search complement each other:

* BM25 is excellent for exact terms, product names, IDs, error codes, acronyms.
* Vector search is excellent for semantic meaning and paraphrases.
* Hybrid search gets the strengths of both.

[5]: https://learn.microsoft.com/en-us/azure/search/search-indexer-overview?utm_source=chatgpt.com "Indexer Overview - Azure AI Search | Microsoft Learn"
[6]: https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index?utm_source=chatgpt.com "Search Index Overview - Azure AI Search | Microsoft Learn"
