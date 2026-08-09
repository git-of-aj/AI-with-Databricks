## The big picture


```text
Agentic Retrieval
│
├── Vector search
├── BM25
├── Reranking
├── Query rewriting
├── Query decomposition
├── Metadata filtering
├── Tool calling
├── Planning
└── Iterative/feedback loops
        │
        ▼
 Intelligent retrieval system
```

## 1. The problem: semantic retrieval assumes one good search

Imagine you're building an AI assistant over your company's documentation.

You ask:

> **"Can I deploy my application to production, and what happens if the deployment fails?"**

Your knowledge base has:

```text
Document A
"Production deployments require two approvals."

Document B
"Applications must pass the security scan before production deployment."

Document C
"Rollback can be performed using the deployment dashboard."

Document D
"If a deployment fails, the platform automatically rolls back
to the previous healthy version."

Document E
"New services require registration with the platform team."
```

A traditional RAG pipeline might do:

```text
Question
   ↓
Embedding
   ↓
Vector DB
   ↓
Top 5 chunks
   ↓
LLM
   ↓
Answer
```

The fundamental assumption is:

> **The user's question can be represented by one search query, and the most similar chunks contain what we need.**

That's often false.

---

# 2. Why?

Look at the question again:

> **"Can I deploy my application to production, and what happens if the deployment fails?"**

This actually contains several questions:

```text
Q1: What are the requirements for production deployment?
Q2: Does my application need security approval?
Q3: What happens when deployment fails?
Q4: Can I recover/rollback?
```

A single embedding doesn't explicitly understand this search strategy.

An agentic system can.

It can say:

```text
                    User question
                         │
                         ▼
                       Agent
                         │
              "This requires multiple
                 pieces of evidence"
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Search #1       Search #2       Search #3
   deployment       security       deployment
   requirements      approval         failure
          │              │              │
          ▼              ▼              ▼
        Doc A          Doc B          Doc D
                                         │
                                         ▼
                                    Search #4
                                  "rollback?"
                                         │
                                         ▼
                                       Doc C
                                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
       Evidence                     Evidence
          │                             │
          └──────────────┬──────────────┘
                         ▼
                       LLM
                         ▼
                      Answer
```

**That's why agentic retrieval exists.**

Not because vector search is bad.

Because **some questions require a search strategy rather than a single search.**

---

Agentic retrieval is similar:

```text
Retrieval primitives
        │
        ├── vector search
        ├── keyword/BM25 search
        ├── metadata filtering
        ├── reranking
        ├── query rewriting
        ├── document fetching
        └── LLM reasoning
                 │
                 ▼
          Agentic Retrieval
```

# 4. What is underneath agentic retrieval?

There are several important building blocks.

### A. Query decomposition

The agent turns:

> "Can I deploy and what happens if it fails?"

into:

```text
"What are the production deployment requirements?"

"What approvals are required?"

"What happens when deployment fails?"

"How do I rollback?"
```

This is usually done by an **LLM**.

---

### B. Query rewriting

Suppose the user asks:

> "What about the approval?"

The word **"approval"** is ambiguous.

The agent knows the conversation was about production deployment.

It might rewrite it as:

```text
"production deployment approval requirements"
```

This makes retrieval much better.

---

### C. Multiple retrieval strategies

This is an important one.

You don't necessarily want only vector search.

You might have:

```text
                  Retriever
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
   Vector         BM25          SQL/filter
   search         search
       │             │             │
       └─────────────┼─────────────┘
                     ▼
                  Results
```

For example:

**Semantic search**

> "deployment failure recovery"

might find:

> "automatic rollback"

because the meanings are related.

But **keyword search** might be better for:

> `"ERR_DEPLOY_403"`

because exact identifiers matter.

Agentic systems can choose between these.

---

# 5. Reranking

Suppose retrieval returns 20 documents.

The agent/system can ask:

> "Which of these 20 are actually relevant?"

A **reranker** scores them.

```text
Vector search
     ↓
20 documents
     ↓
Reranker
     ↓
Document 7   0.94
Document 2   0.91
Document 14  0.88
Document 5   0.72
     ↓
Top 3
```

So you often get:

```text
Broad retrieval → reranking → useful evidence
```

rather than simply:

```text
Vector search → top 5
```

---

# 6. Tool calling

This is where it starts becoming genuinely "agentic."

An agent can have tools such as:

```python
tools = [
    search_documents,
    search_wiki,
    search_code,
    query_database,
    get_service_config,
]
```

The LLM decides:

```text
"I need the deployment policy."
        ↓
search_documents()

"I need the current deployment status."
        ↓
query_database()

"I need to know how rollback works."
        ↓
search_documents()
```

This is **tool calling/function calling**.

It's one of the fundamental mechanisms behind agentic systems.

---

# 7. The really important concept: the retrieval loop

This is probably the single most important concept to understand.

Traditional RAG:

```text
Question
   ↓
Retrieve
   ↓
Generate
```

Agentic retrieval:

```text
Question
   ↓
Plan
   ↓
Retrieve
   ↓
Inspect results
   ↓
Do I have enough information?   ======> Feedback loop 
   │
   ├── NO ──→ Rewrite query
   │            ↓
   │         Retrieve again
   │            ↓
   │         Inspect again
   │
   └── YES
        ↓
      Answer
```

That's why it's **agentic**.

There is a **feedback loop**.

---

Now the LLM controls the loop:

```text
                 ┌──────────────────┐
                 │       LLM        │
                 │                  │
                 │ "What do I need?"│
                 └────────┬─────────┘
                          │
                    tool selection
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Vector         BM25       Database
          Search         Search       Query
             │            │            │
             └────────────┼────────────┘
                          ▼
                       Results
                          │
                          ▼
                         LLM
                          │
                ┌─────────┴─────────┐
                │                   │
             Enough?              Not enough
                │                   │
                ▼                   └──────→ search again
              Answer
```

That is the core architecture.

---

# 10. The stack you should learn

If you're trying to understand this technically, I'd learn the components in this order:

```text
                    AGENTIC RETRIEVAL
                           │
            ┌──────────────┴──────────────┐
            │                             │
        Agent/LLM                    Retrieval
            │                             │
     ┌──────┼──────┐              ┌───────┼───────┐
     │      │      │              │       │       │
   Planning Tools Memory       Embedding BM25  Metadata
     │      │      │              │       │       │
     │      │      │              ▼       ▼       ▼
     │      │      │          Vector DB Search Engine
     │      │      │
     └──────┴──────┘
            │
       Tool calling
            │
            ▼
       Retrieval loop
```

The concepts worth knowing are:

1. **Embeddings** — represent meaning numerically.
2. **Vector databases** — find semantically similar chunks.
3. **BM25/keyword search** — exact/lexical retrieval.
4. **Metadata filtering** — restrict search by things like department/date/document type.
5. **Reranking** — improve the ordering of retrieved results.
6. **Query rewriting** — turn vague questions into better searches.
7. **Query decomposition** — break complex questions into subquestions.
8. **Tool/function calling** — let an LLM invoke retrieval or other systems.
9. **Planning** — decide which searches/tools are needed.
10. **Reflection/verification** — inspect whether retrieved evidence is sufficient.
11. **Iterative retrieval** — search again based on what was discovered.
12. **Context assembly** — give the final evidence to the answering LLM.

---



