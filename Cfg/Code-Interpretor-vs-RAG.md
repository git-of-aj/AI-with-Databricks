
| Scenario                                   | Code Interpreter     | RAG                             |
| ------------------------------------------ | -------------------- | ------------------------------- |
| User uploads 2–5 PDFs and asks questions   | ✅ Excellent          | Possible, but often unnecessary |
| User uploads Excel, CSV, financial data    | ✅ Best choice        | Not needed                      |
| Need charts, calculations, Python analysis | ✅ Best choice        | ❌                               |
| Hundreds or thousands of documents         | ❌ Doesn't scale well | ✅ Best choice                   |
| Persistent knowledge base                  | ❌ Session-based      | ✅                               |
| Fast semantic search across documents      | ❌                    | ✅                               |
| Need citations from many documents         | Limited              | ✅                               |


```txt
Small upload (≤10 files)
        │
        ▼
Code Interpreter
        │
        ▼
Answer

----------------------------------

Large knowledge base
        │
        ▼
Vector Search (RAG)
        │
        ▼
Retrieve relevant chunks
        │
        ▼
LLM
        │
        ▼
(Optional) Code Interpreter for calculations/charts

```
