
## Agent Creation lifecycle:
Doc: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/development-lifecycle
1. Use this lifecycle as a practical checklist while you build and ship an agent.
2. Choose an agent type: Start with a prompt-based agent, a workflow, or a Hosted agent.
3. Create your agent and start testing: Iterate in the playground or in code.
4. Add tools and data: Attach tools for retrieval and actions, and validate the configuration before you save.
5. Save changes as versions: Capture meaningful milestones and compare versions.
6. Debug with tracing: Use tracing to confirm tool calls, latency, and end-to-end behavior. For details, see Agent tracing overview.
7. Evaluate quality and safety: Run repeatable evaluations to catch regressions before publishing. For conceptual guidance, see Agent evaluators.
8. Optimize hosted agents (preview): Automatically improve your hosted agent's instructions and discover skills using the agent optimizer.
9. Publish and integrate: Publish a stable endpoint and integrate it into your application. For steps, see Agent applications in Microsoft Foundry.
10. Monitor and iterate: Monitor performance and quality in production, then update and republish as needed. For guidance, see Monitor agents.

## Agent Identity
`agent identity` is a specialized identity type in Microsoft Entra ID that's designed specifically for AI agents.enables agents to securely access resources, interact with users, and communicate with other systems.

`Agent Identity Blueprint`: Group of agent identity: 
- Type classification: The blueprint establishes the category of agent, such as "Contoso Sales Agent." This classification enables administrators to:
- Apply Conditional Access policies to all agents of that type.
- Disable or revoke permissions for all agents of that kind.
- Audit and govern agents at scale through consistent, blueprint-based controls.

## AI Search (foundry IQ)
```txt
QUERY
authenticate users

DOCUMENT
identity subsystem validates OAuth 2.0 bearer credentials
```
- Key word search struggles here
```txt
embedding("authenticate users")
                 ↕
embedding("identity subsystem validates OAuth credentials")
```
- That's one of the fundamental reasons Azure AI Search combines keyword + vector + semantic ranking for high-quality retrieval
- `Enable Text Vectorization` In Azure AI search means:
- "Take the textual content of my indexed documents and create semantic vector representations so Azure AI Search can retrieve content based on meaning, not just matching words."
- `Enable Image Verbalization`
- An LLM looks at the image in your PDF and generates a textual description such as:
"An architecture diagram showing a client sending requests to an API Gateway, which forwards requests to an Authentication Service."
That generated text is called the verbalization.
> Image verbalization uses an LLM to generate natural-language descriptions, and an embedding model then vectorizes the plain text and verbalized images.
```txt
                 IMAGE
                   │
                   ▼
          ┌─────────────────┐
          │   LLM analyzes  │
          │     image       │
          └────────┬────────┘
                   │
                   ▼
        "Architecture diagram
         showing API Gateway
         connected to Auth..."
                   │
                   ▼
          TEXT VECTORIZATION
                   │
                   ▼
             EMBEDDING
                   │
                   ▼
          VECTOR IN SEARCH INDEX
```

| Capability                                      | Main purpose                                              |
| ----------------------------------------------- | --------------------------------------------------------- |
| **Text vectorization**                          | Make text semantically searchable                         |
| **Image verbalization**                         | Turn visual information into searchable text              |
| **Image vectorization / multimodal embeddings** | Represent images directly as vectors                      |
| **Image serving**                               | Give the actual image to the LLM during answer generation |
| **OCR**                                         | Extract literal text appearing inside images              |
| **Semantic ranking**                            | Rerank retrieved results for relevance                    |
| **Agentic retrieval**                           | Plan/decompose queries and orchestrate retrieval          |

**Imagine a financial report containing:**

**Text**  
"Revenue increased 17% in FY2025."

**Chart**  
📊 Revenue by year: 2023 → 2024 → 2025

**Architecture diagram**  
🖼️ Data flows from ERP → Data Lake → Analytics Platform.

**With Text Vectorization:**

```text
"Revenue increased 17%..."
              ↓
          embedding
              ↓
          vector index
```

**With Image Verbalization:**

```text
Revenue chart
      ↓
     LLM
      ↓
"Chart shows revenue increasing..."
      ↓
 embedding
      ↓
vector index
```

**Then a user asks:**

> "How did revenue change and what system processes the financial data?"

**Agentic retrieval can retrieve:**

```text
TEXT CHUNK
"Revenue increased 17%..."

+

IMAGE-DERIVED DESCRIPTION
"Revenue chart shows..."

+

IMAGE-DERIVED DESCRIPTION
"Diagram shows ERP feeding the data lake..."
```

The agent/LLM can then formulate the answer from those retrieved pieces.

That's the underlying idea: **convert heterogeneous enterprise content into representations that the retrieval system can effectively search, then let agentic retrieval select the right pieces for the LLM.**

Microsoft's current documentation recommends this kind of content preparation because **RAG quality depends heavily on how well the source content is chunked, vectorized, and enriched before retrieval.**
