> Agenda : platform basics → models → endpoints/SDKs → chat app development → optimization → responsible AI.

## what changed with chatgpt release in 2022?
- Classic ML: Learn a mapping input → prediction (f(x)=y).
- Generative AI: Learn patterns from data to understand language, reason about requests, and generate new content (text, code, images, etc.).
- **Traditional AI = Calculator**
1. Designed for specific operations
2. Extremely reliable within its scope.

**LLMs = Universal language interface**
1. Can perform many different knowledge and communication tasks.
2. More flexible, but also more prone to mistakes.

- Model: The entire machine.
- Parameters: The knobs inside the machine.

For a radio:

The radio = model
The tuning settings = parameters

Training is the process of adjusting all the knobs until the radio receives the signal clearly. For an LLM, there may be hundreds of billions of such "knobs."

```sh
Input
  ↓
Neuron
  ↓
Neuron
  ↓
Output
```
- each neuron has parameter that it learns over trainig
```sh
  Input --0.7--> Neuron
Input --1.3--> Neuron
Neuron --2.1--> Output
```
> More parameters (Means models has read more books... but depends on book quality [aka training data] and how fast he navigates [training weights and biases] and access it [compute and other infra]) usually give a model the potential to be more capable because it can store and manipulate more learned patterns. However, a model is not smarter just because it has more parameters; training data, architecture, optimization, and post-training techniques are often just as important, and sometimes more important.

**GPU vs CPU**:
Think of an LLM as a giant network of matrix multiplications.

- CPU = a few extremely capable engineers.
- GPU = a huge factory with thousands of workers all multiplying numbers simultaneously.
- Companies such as NVIDIA dominate AI because their GPUs provide:

- Massive parallel computation
- High-speed VRAM
- Fast communication between GPUs
- Software tools optimized for AI training

Training a modern LLM is often limited by:

- GPU compute power
- GPU memory
- GPU-to-GPU communication speed

- rather than CPU speed.

In fact many small AI models run on CPUs.

Examples:

- Local chatbots
- Small language models
- Traditional ML systems

But they are much slower. A task taking: `1 second on GPU `might take: `10–100+ seconds on CPU` depending on the workload.

## Open Weights vs Open Source Model
Open Source AI

A truly open-source AI model would provide:

✅ Model architecture (how it's built)
✅ Training code
✅ Training recipes
✅ Datasets (or dataset details)
✅ Model weights

Like open-source software where you can inspect everything.

Example:

- PyTorch
- TensorFlow

## Ai Terms:
> Token → Embedding (vector) → Processed by parameters/weights → Next token prediction.
**One-Line Definitions**
- Token = chunk of text.
- Vector = list of numbers.
- Embedding = vector representing meaning of a token/concept.
- Weight = learned connection strength inside a neural network.
- Parameter = any learnable number in the model (weights, biases, embeddings, etc.).
- Open-weight model = weights are publicly available.
- Open-source model = weights + code + training details (and ideally data) are available.

## How Text to tokens (tiktoken) => Vectors + Embedding (text-3-small):
You're thinking about the pipeline correctly. The key point is:

> **Tokenization and embeddings solve different problems. You cannot skip embeddings/vectorization in modern neural networks.**

The flow is:

```text
Text
 ↓
Tokenization
 ↓
Token IDs
 ↓
Embeddings (vectors)
 ↓
Transformer layers
 ↓
Output tokens
```

---

# Why Not Feed Text Directly?

Computers don't understand text.

Suppose you write:

```text
dog
```

The neural network can't multiply or add the letters:

```text
d
o
g
```

It only works with numbers.

So we need a conversion process.

---

# Step 1: Tokenization

### Problem It Solves

Convert raw text into manageable pieces.

Example:

```text
I love dogs.
```

might become:

```text
["I", " love", " dogs", "."]
```

Each token gets an ID:

```text
"I"      → 42
" love"  → 831
" dogs"  → 6121
"."      → 13
```

Now the sentence becomes:

```text
[42, 831, 6121, 13]
```

---

### Why Not Use Whole Words?

Because language is huge.

Imagine storing every possible word:

```text
running
runner
runners
unhappiness
ChatGPT
...
```

Millions of possibilities.

Instead tokenizers break text into reusable pieces.

For example:

```text
unhappiness
```

could become:

```text
["un", "happy", "ness"]
```

This dramatically reduces vocabulary size.

---

# Step 2: Embeddings

Now we have:

```text
[42, 831, 6121, 13]
```

But these IDs have no meaning.

The model doesn't know:

```text
42 and 43 are unrelated
```

because token IDs are arbitrary labels.

For example:

```text
dog   = 6121
cat   = 97
```

The numbers themselves don't tell us anything.

---

### Problem Embeddings Solve

Convert token IDs into meaningful numerical representations.

Example:

```text
dog
```

becomes

```text
[0.7, -1.2, 0.4, ...]
```

and

```text
puppy
```

becomes

```text
[0.8, -1.1, 0.5, ...]
```

These vectors end up close together.

Now the model can recognize similarity.

---

# Why Vectors Are Necessary

Neural networks are giant matrix multiplication machines.

A transformer repeatedly performs operations like:

[
Y = XW
]

Y=XW

Matrix multiplication requires vectors and matrices.

You cannot multiply:

```text
dog × cat
```

but you can multiply:

```text
[0.7, -1.2, 0.4] × matrix
```

So embeddings are the bridge between language and math.

---

# Are Embeddings and Vectorization the Same?

People often use the terms loosely.

### Vectorization

General process:

```text
Anything
 ↓
Vector
```

Could be:

* text
* image
* audio

---

### Embedding

A specific learned vector representation.

So:

```text
Embedding ⊂ Vectorization
```

Every embedding is a vector.

Not every vector is an embedding.

---

# During Training

Initially:

```text
dog
```

might map to:

```text
[0.01, -0.03, 0.02]
```

basically random.

Training gradually adjusts embedding values.

After seeing billions of examples:

```text
dog
```

and

```text
puppy
```

naturally move closer together.

The embedding table itself is learned.

---

# Where Are Embeddings Stored?

Inside the model parameters.

A simplified embedding table:

| Token | Vector           |
| ----- | ---------------- |
| dog   | [0.7, -1.2, ...] |
| cat   | [0.6, -1.1, ...] |
| Paris | [1.8, 0.4, ...]  |

This table is part of the model.

---

# What Tools Create Tokenizers?

Common tokenizer libraries:

### Hugging Face Tokenizers

[Hugging Face Tokenizers](https://github.com/huggingface/tokenizers?utm_source=chatgpt.com)

Widely used in LLMs.

---

### SentencePiece

[SentencePiece](https://github.com/google/sentencepiece?utm_source=chatgpt.com)

Used by many Google and open-weight models.

---

### TikToken

[TikToken](https://github.com/openai/tiktoken?utm_source=chatgpt.com)

OpenAI tokenizer library.

---

# What Creates Embeddings?

Embeddings are usually learned automatically during model training.

Frameworks:

* [PyTorch](https://pytorch.org?utm_source=chatgpt.com)
* [TensorFlow](https://www.tensorflow.org?utm_source=chatgpt.com)
* [JAX](https://jax.dev?utm_source=chatgpt.com)

Example in PyTorch:

```python
embedding = nn.Embedding(
    vocab_size=50000,
    embedding_dim=4096
)
```

This creates an embedding matrix.

Training learns the values.

---

# What About Standalone Embedding Models?

Sometimes you don't want a chatbot.

You just want vectors for search or retrieval.

Examples:

* [Sentence Transformers](https://www.sbert.net?utm_source=chatgpt.com)
* [Cohere Embed](https://cohere.com?utm_source=chatgpt.com)
* [OpenAI Embeddings](https://platform.openai.com?utm_source=chatgpt.com)

Input:

```text
How do I learn Python?
```

Output:

```text
[0.18, -0.91, 1.22, ...]
```

These vectors are then stored in vector databases for semantic search.

---

# The Mental Model

Think of it this way:

### Tokenization

**Problem:** Break language into machine-readable pieces.

```text
Text → Token IDs
```

---

### Embedding

**Problem:** Give those pieces mathematical meaning.

```text
Token IDs → Meaningful vectors
```

---

### Transformer Layers

**Problem:** Reason over those vectors and predict what comes next.

```text
Vectors → New vectors → Output
```

So the answer to your main question is:

> **No, modern LLMs do not skip vector generation. Tokenization converts text into token IDs, and embeddings then convert those IDs into vectors. Those vectors are the actual inputs consumed by the neural network.** Tokenization and embeddings solve different problems, and both are essential parts of the pipeline.
---
# Section:2 | Microsoft Foundry Models

- [Pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry-models/grok/)
> Select Model > Deploy
- By default, the deployment uses the model name. You can modify this name before deploying.
- During inference, the deployment name is used in the model parameter to route requests to this particular deployment.

**Deployment**:
Deployment type that determines:

- Where your data is processed (global, data zone, or single region)
- How you pay (pay-per-token or reserved capacity)
- Performance characteristics (latency variance, throughput limits)
- The service offers two main categories: standard (pay-per-token) and provisioned (reserved capacity). Within each category, you can choose global, data zone, or regional processing based on your compliance requirements.

**Selected Region is used but:** 
> Data stored at rest remains in the designated Azure geography. However, inferencing data is processed as follows:

- Global types: May be processed in any Azure region
- DataZone types: Processed only within the Microsoft-specified data zone (US or EU)
- Standard/Regional types: Processed in the deployment region

[MS Docs Flow chart which when to use](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types#choose-the-right-deployment-type)
> Restrict deployment types with Azure Policy

`Instant Models - no need to deploy.. use straight away -- only for POC !!`
- During the preview, instant models are available in projects in `West US 3` only as of date: 14 June 2026. [MS Docs](https://learn.microsoft.com/en-us/azure/foundry/concepts/instant-models?tabs=python%2Crest-api)
- Training = Studying for an exam.
- Inference = Taking the exam and answering questions based on what you've learned.
For large language models like ChatGPT, inference means predicting the next word (or token) repeatedly to generate a complete response.

*Compare Models*
![](https://learn.microsoft.com/en-us/training/wwl-data-ai/model-catalog-evaluate/media/chat-playground.png)

### SDK and Endpoint
**One-line Memory Trick**

**Foundry = Project-centric + Entra ID + Responses API**
**Azure OpenAI = Full OpenAI surface + Entra/API Key + Responses/Chat Completions**

#### Choosing an Endpoint and SDK (Azure AI Foundry vs Azure OpenAI)

#### Quick Decision Rule

* **Use Foundry Project Endpoint + Microsoft Foundry SDK** when you need:

  * Foundry-native project operations
  * OpenAI-compatible interfaces for **Foundry direct models**
* **Use Azure OpenAI Endpoint + OpenAI SDK** when you need:

  * Full OpenAI API surface
  * Latest OpenAI SDK features
  * Broader model support

> **Endpoint choice drives authentication and API surface.**

---

#### Comparison Table

| Aspect             | Foundry Project                                      | Azure OpenAI                                            |
| ------------------ | ---------------------------------------------------- | ------------------------------------------------------- |
| **Endpoint**       | Project endpoint (`.../api/projects/{project-name}`) | Azure OpenAI endpoint (`...openai.azure.com/openai/v1`) |
| **SDK**            | Microsoft Foundry SDK (`azure-ai-projects`)          | OpenAI SDK (`openai`)                                   |
| **Authentication** | Microsoft Entra ID only                              | Microsoft Entra ID or API Key                           |
| **Chat API**       | Responses API                                        | Responses API or Chat Completions API                   |
| **Best For**       | Foundry-specific capabilities and direct models      | Full OpenAI functionality and latest features           |

---
## Tools 
- Use tools like remote MCP servers or web search to extend the model's capabilities else models answers only based on its training data. Play here: https://aistudio.google.com/prompts/new_chat
<img width="1531" height="638" alt="image" src="https://github.com/user-attachments/assets/d69f5e66-1c7e-4ba1-b41a-571aa3a50539" />

> By default, the model chooses when to use a tool (and which one), based on the prompt. You can configure tool selection rules and use the Instructions (system prompt) parameter to guide this choice.

Some of the commonly used tools available in the Responses API, include:

- code_interpreter: A Python environment in which the model can generate and run code.
- web_search: A tool that enables the model to find general information on the Internet, which allows it to base responses on more current data than it was trained on.
- file_search: A tool that enables the model to search specific files that you upload to a dedicated vector search index - enabling it to ground responses in specific knowledge.
- function: A tool that enables the model to call custom functions in your application code.
> 💡specify one or more tools in a call to the responses.create() method when generating a response from a model.

| Tool                                                                        | Who writes the code? | Who executes it?                  |
| --------------------------------------------------------------------------- | -------------------- | --------------------------------- |
| **Function Calling**                                                        | You (the developer)  | Your application/backend          |
| **Code Interpreter** (aka Computer Use / Python tool depending on platform) | The LLM              | A sandboxed execution environment |

| Dimension                    | OpenAI `file_search`                            | Custom RAG                                                            | Real-World Example                                                                                                                   |
| ---------------------------- | ----------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Setup & Speed**            | Upload files and start querying quickly.        | Build ingestion, embeddings, retrieval pipelines.                     | **file_search:** Internal HR policy chatbot in a day. **Custom RAG:** Enterprise search platform built over months.                  |
| **Data Sources & Freshness** | Best for static uploaded documents.             | Can connect to live databases, APIs, CRMs, and knowledge tools.       | **file_search:** Employee handbook Q&A. **Custom RAG:** Customer support agent pulling real-time order status.                       |
| **Control & Optimization**   | Limited control over retrieval behavior.        | Full control over chunking, reranking, hybrid search, Graph RAG, etc. | **file_search:** Simple document lookup. **Custom RAG:** Legal research system using advanced ranking and citations.                 |
| **Operations & Cost**        | Fully managed, low maintenance.                 | Requires infrastructure, monitoring, and ongoing maintenance.         | **file_search:** Startup prototype with minimal engineering effort. **Custom RAG:** Large enterprise managing millions of documents. |
| **Best Use Cases**           | Knowledge assistants, document Q&A, prototypes. | Enterprise search, regulated industries, complex AI agents.           | **file_search:** Company wiki chatbot. **Custom RAG:** Bank compliance assistant with audit and governance requirements.             |

## Now its not just LLM its about agents..
> Prompt engineering focuses on what you ask the model. Context engineering focuses on everything the model knows while answering.
| Prompt Engineering           | Context Engineering                                                  |
| ---------------------------- | -------------------------------------------------------------------- |
| Wording the instruction      | Managing all information available to the model                      |
| Focuses on prompts           | Focuses on information flow                                          |
| "Act as a teacher"           | "Give the model the student's history, curriculum, and test results" |
| Usually a single interaction | Often a complete system architecture                                 |

> “If answers are wrong → add grounding. If answers are messy/inconsistent → tighten prompts or fine-tune.”
As a general guide, most solutions benefit primarily from prompt engineering. RAG is useful if you have context-specific data you want the model to take account of, and fine-tuning is used only when you can’t achieve the required tone and style in your model responses through prompt engineering. In terms of cost, prompt engineering incurs the lowest cost, followed by RAG as you need to pay for data storage and index hosting. Finally, fine-tuning is usually the most expensive option due to the compute overhead required to perform the training.

- **system prompts as “role + constraints + output format expectations.**
> ChatGPT is fundamentally a Large Language Model (LLM) at its core, but it operates as an AI agent through its additional built-in systems, integrations, and tools. 
# Foundry Agents
<img width="1456" height="715" alt="image" src="https://github.com/user-attachments/assets/c69b3a1a-f309-4982-9893-61a60147209e" />

> Actions speak louder than work.. Agent do work while Models Jsut talk.
`An agent is an AI application that uses a model from the Foundry model catalog to reason about user requests and take autonomous actions to fulfill them`
There are two main agent types in Agent Service:

1. Prompt agents — author in portal or code, fully managed runtime.
2. Hosted agents (preview) — your agent code, run by Foundry.
3. Agents running on AKS, Langraph etc use reponse API from Foundry to give them LLM access.

- `Foundry` Agent Service provides built-in tools and supports custom tools so your agents can take actions and access data.
- `Collection / Folder of tools... Easy to share`: Toolbox lets you define a curated set of tools once, manage them centrally in Foundry, and expose them through a single MCP-compatible endpoint.
- Each agent can have a dedicated Microsoft Entra identity, enabling secure, scoped access to resources and APIs without sharing credentials
> usually you add skills to agent like MS officially published skills for coding agents: https://github.com/microsoft/azure-skills
- [IBM: Types of AI Agents](https://www.ibm.com/think/topics/ai-agent-types)
## Glue the agent logic together
[Microsoft Agent Framework](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/) and its [docs](https://learn.microsoft.com/en-us/agent-framework/overview/?pivots=programming-language-python)
OR Use alternatives
- LangGraph (with LangChain) is the gravity well. It’s a graph-based agent runtime with the biggest ecosystem, the most integrations, and a steep learning curve. Strong for stateful, branching agents that need persistence and human-in-the-loop steps. Weakness: a sprawling API surface and a reputation, partly earned, for breaking changes. Use it when your flow is genuinely complex.

- OpenAI Agents SDK is the lightweight, opinionated alternative. Built-in tracing, handoffs between agents, guardrails. Cleanest path if your stack is OpenAI-first or near-first. It’s now model-agnostic enough to use with Claude and others, but its developer experience shines brightest in the OpenAI ecosystem.

- CrewAI is the role-based multi-agent framework. You define agents with roles, goals, and tools, then a process for how they collaborate. Good for prototyping crew-like workflows. The honest critique: many CrewAI projects would be faster and more reliable as a single agent with the right tools
> The reason these three matter more than anything else is that they decide which set of frameworks you’re even shopping in. A TypeScript team should not be evaluating CrewAI. A visual-builder team should not be reading LangGraph docs. Saying these out loud at the start of a project saves entire weeks.
Most teams choose one too early.

Before picking LangGraph, CrewAI, Microsoft Agent Framework, LlamaIndex Workflows, OpenAI Agents SDK or Google ADK, I would ask:

- Where does state live?
- Who approves risky actions?
- How do we replay failures?
- How do we debug tool calls?
- How do we stop runaway cost?
- Can this run in our deployment environment?

Frameworks help, but they do not remove architecture.

- LangGraph gives explicit control.
- CrewAI gives a simple collaboration model.
- LlamaIndex is strong near data/RAG.
- Microsoft Agent Framework makes sense for Microsoft-centric shops.
- OpenAI Agents SDK is the safer current OpenAI path.
- Google ADK fits Gemini/Google Cloud teams.

`The best harness is the one your team can operate at 2 AM.`

# AI Agent or AI Workflow - whats better?
source: https://aishwaryasrinivasan.substack.com/p/all-you-need-to-know-about-ai-agent
- A workflow is a predetermined sequence of LLM calls. You wrote the steps. The model fills in the content. Predictable, debuggable, cheap.
- An agent is a loop where the model itself decides the next step. It picks tools, retries, branches. Flexible, but slower, more expensive, and harder to debug.
- The rule almost nobody follows: prefer workflows. Reach for agents only when the task genuinely cannot be predetermined, which is a smaller share of real use cases
