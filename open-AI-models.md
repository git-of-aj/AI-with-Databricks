contract driven api development vs spec driven development
GitHub MOdels
Completeion API
Inference SDK Azuer AI

> It's your responsibility to ensure that the prompt and completion fall within the token limit. For longer conversations, you need to keep track of the token count and only send the model a prompt that falls within the limit. Alternatively, with the responses API you can have the API handle truncation/management of the conversation history for you.


Common errors
401/403 (authentication): Verify your API key, or confirm you have Microsoft Entra ID access to the Azure OpenAI resource.
400/404 (deployment not found): Confirm that model matches your deployment name.
Invalid URL: Confirm that base_url ends with /openai/v1/.

Links:
Pricing: https://developers.openai.com/api/docs/models
Parameters in Popular LLMs: https://www.ibm.com/think/topics/large-language-models-list
responses API: https://youtu.be/3Z03fwH1I7s?si=gfQiO_wzHLMJZz7t
Foundry Models Response API: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses?tabs=python

Labs:
- Build AI agents with portal and VS Code: https://microsoftlearning.github.io/mslearn-ai-- agents/Instructions/Exercises/01-build-agent-portal-and-vscode.html
- Apply guardrails to prevent the output of harmful content: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/06-Explore-content-filters.html
- Create a generative AI app that uses tools: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/04a-use-own-data.html
- Create a generative AI chat app: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/03-foundry-sdk.html
- Explore and compare models: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/02-model-catalog-evaluation.html
- Prepare for an AI development project: https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/01-Explore-ai-studio.html

---
It is entirely fair to be confused by this. Every AI company—whether it is OpenAI, Anthropic, DeepSeek, X.AI (Grok), or Cohere—likes to invent their own marketing terms. However, under the hood, the underlying computer science and the types of models they offer are fundamentally the same.

### **Summary Comparison**

| Model/API Type | Input | Output | Primary Purpose |
| --- | --- | --- | --- |
| **Chat Completion** | A structured transcript of messages. | Generated text (the next message). | Having a conversation, answering prompts, writing code. |
| **Responses / Agents** | A prompt + access to tools. | Generated text + executed actions. | Automating complex, multi-step workflows with memory. |
| **Embedding** | Raw text. | A list of numbers (a vector). | Measuring how similar two pieces of text are to each other. |
| **Classification** | Raw text + predefined labels. | A category or a probability score. | Sorting, tagging, and organizing large amounts of text. |

---

### **1. Chat Completions (The Conversationalist)**

* **What it is:** A model endpoint specifically fine-tuned to understand back-and-forth dialogue.
* **How it works:** Instead of sending a single block of text, you send a highly structured list of messages with specific roles (e.g., `System`, `User`, `Assistant`). The AI looks at the entire transcript and predicts the next logical response from the "Assistant."
* **Industry Examples:** DeepSeek Chat, Grok's standard API, Anthropic's Messages API, Llama 3 Chat.
* **Best for:** Building chatbots, interactive agents, and any task where maintaining the flow of a human-to-AI conversation is required.

### **2. Responses / Unified APIs (The Orchestrator)**

* **What it is:** "Responses" (or similar terms like "Agents" or "Unified Endpoints") usually refer to the **API layer rather than the model itself**. It is a modern wrapper around chat models that handles extra logic for you.
* **How it works:** Instead of just taking text and returning text, a Responses API manages the "state" (memory) on its own servers and can autonomously route tasks. If you ask it a question, the Response API might decide to trigger a web search, run some Python code, and *then* use a Chat Completion model to format the final answer.
* **Industry Examples:** OpenAI’s Responses API, Cohere’s multi-step tool use, Google's Gemini API with built-in grounding.
* **Best for:** Building complex AI agents that need memory, file access, and the ability to use external tools without you having to code all the infrastructure yourself.

### **3. Embedding Models (The Translator to Math)**

* **What it is:** A model that does not generate words at all. Instead, it translates text (or images/audio) into a massive array of numbers (called a vector).
* **How it works:** Think of an embedding model as plotting words on a massive 3D map based on their meaning. "Dog" and "Puppy" are plotted right next to each other; "Dog" and "Carburetor" are plotted far apart.
* **Industry Examples:** Nomic Embed, Cohere Embed, Voyage AI, DeepSeek's embedding models.
* **Best for:** Search engines, recommendations, and **RAG** (Retrieval-Augmented Generation). If you want your AI to "read" your company's 10,000-page PDF manual, you don't paste it into a chat. You turn the manual into embeddings, search for the mathematical "closest" paragraphs to the user's question, and feed only those paragraphs to the Chat Completion model.

### **4. Classification Models (The Sorter)**

* **What it is:** A model designed to read text and assign it a specific label or category, rather than generating a creative response.
* **How it works:** Generative models (like chat) are computationally expensive and sometimes hallucinate. If you just need to know if an email is "Spam" or "Not Spam," you use a classification model. You give it a list of categories, and it outputs the probability of the text belonging to each one.
* **Industry Examples:** Cohere Classify (which is famous for this), standard BERT models on HuggingFace.
* **Best for:** Sentiment analysis (Positive/Neutral/Negative), intent recognition (e.g., routing customer support tickets to "Billing" or "Tech Support"), and content moderation.

---
Here is a breakdown of what **"Compacting a Response"** means in the context of AI and stateful APIs:

### **The Problem: The Expanding Context Window**

When you have a back-and-forth (multi-turn) conversation with an AI, the system has to "read" the entire history of the chat every single time you send a new message so it knows what you are talking about.

As the conversation gets longer, two problems occur:

1. **Cost and Speed:** You are charged per token (word/piece of a word). Sending a massive chat history back and forth gets expensive and slows the AI down.
2. **Memory Limits:** AI models have a strict limit on how much text they can process at once (the "context window," like 128k tokens). Eventually, a long conversation will hit a wall and crash.

### **The Solution: Compaction**

**Compaction** is the automated process of shrinking that massive conversation history down to a smaller size, without making the AI forget what you were talking about.

Here is what the two halves of that sentence actually mean:

#### **1. "Reduces the input context..."**

Instead of keeping the exact, word-for-word transcript of every single message sent since the conversation started, the system automatically removes or trims down the oldest parts of the chat. It significantly lowers the total number of tokens (the "input context") being sent to the model.

#### **2. "...while preserving essential state for later turns."**

The AI doesn't just blindly delete old messages. Instead, it usually **summarizes** them. It extracts the crucial facts, user preferences, and the core goal of the conversation (the "essential state") and keeps *that* in its memory for future messages ("later turns").

### **A Real-World Analogy**

Imagine you are in a two-hour business meeting.

* **Without compaction:** To remember what happened, you have to read a 50-page, word-for-word transcript of everything everyone said. It takes forever.
* **With compaction:** You read a half-page summary of the "Key Takeaways and Action Items." You lose the exact jokes and small talk (reduced context), but you still know exactly what project you are working on and what needs to be done next (preserved state).

----------
## Notepad RAW 
OpenAI trained chat completion models to accept input formatted as a conversation. The messages parameter takes an array of message objects with a conversation organized by role. When you use the Python API, a list of dictionaries is used.

{"role": "assistant", "content": "Provide some context and/or instructions to the model"},
{"role": "user", "content": "The user's message goes here"}

if 12 banana cost 50 rupees, i had only a 100 ruppee note the shopkeeper says he do not have the change, we both were confused what to do, then he said buy banana of 100 rupee, I refused, then I bought a icecream of Rs 35, but he gave me back one coin of Rs 5, 3  note of Rs 20, banana shopkeeper had no change of Rs 10, so how many banana can I purchase for rs 60?  

https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/chatgpt?tabs=python-secure%2Cdotnet-secure&pivots=programming-language-python#system-role

system role: If you need to include only a small amount of information, you can hard code it in the system message. If you have a large amount of data that the model should be aware of, you can use embeddings or a product like Azure AI Search to retrieve the most relevant information at query time.

After the system role, you can include a series of messages between the user and the assistant.

If you need to include only a small amount of information, you can hard code it in the system message. If you have a large amount of data that the model should be aware of, you can use embeddings or a product like Azure AI Search to retrieve the most relevant information at query time.

Use chat completion for nonchat scenarios
{"role": "system", "content": "You are an assistant designed to extract entities from text. Users will paste in a string of text and you will respond with entities you've extracted from the text as a JSON object. Here's an example of your output format:
{
   "name": "",
   "company": "",
   "phone_number": ""
}"},
{"role": "user", "content": "Hello. My name is Robert Smith. I'm calling from Contoso Insurance, Delaware. My colleague mentioned that you are interested in learning about our comprehensive benefits policy. Could you give me a call back at (555) 346-9322 when you get a chance so we can go over the benefits?"}

