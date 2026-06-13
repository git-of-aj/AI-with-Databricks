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
