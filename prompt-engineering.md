## Prompt Guide
- Why: Sometimes we do not get expected answer : Either Bad Quality or Less than expected
- We want 2 be sure should we change Model or Just ask better questions :)
- Real World Harsh Truth: Same Promting Guide is not for Every Model, Like long prompts in GPT-5.5 is waste of time vs older models [OpenAI Docs](https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5)
- Every Model (Gemini/Opus/GPT): has their own style and settings to get best results. [Evidence]


---

## Types of Prompt - User Prompt vs System Prompt 

## Best practice of System Prompt:
![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F0442fe138158e84ffce92bed1624dd09f37ac46f-2292x1288.png&w=3840&q=75)


## 1. Inspecting Logs and Troubleshooting Errors (Context Engineering)

### ❌ The Bad Prompt

> Why is my Kubernetes pod crashing with an OOMKilled error?

### 🎯 The Structured (Good) Prompt

> **Role:** You are a Senior DevOps Engineer.
> **Context:** A Kubernetes pod running a Python data processing script is repeatedly crashing.
> **Logs:** [Paste the last 50 lines of the pod logs here, including the exact error stack trace].
> **Task:** Analyze these logs and identify the root cause of the crash.
> **Output Requirements:**
> 1. State the specific function or line of code causing the memory spike.
> 2. Provide the exact `kubectl` command to temporarily increase the memory limit for this specific deployment to mitigate the issue while we fix the code.
> 
> 

### 💡 The Visible Difference in Output

* **Bad Output:** The LLM gives you a high-level, textbook definition of what "Out of Memory" means and lists 10 generic reasons a pod might crash. You learn nothing new.
* **Structured Output:** The LLM reads the stack trace, identifies that your Python script is trying to load a massive dataset into memory all at once instead of chunking it, and provides the exact `kubectl patch deployment` command you need to keep the service alive.

---

## 2. Clarifying Architecture and Tooling (Role-Based & Context Formatting)

### ❌ The Bad Prompt

> Explain Databricks Unity Catalog.

### 🎯 The Structured (Good) Prompt

> **Role:** Act as a Principal Data Architect.
> **Task:** Explain the core purpose of Databricks Unity Catalog to an IT Operations engineer who is very experienced with Azure DevOps and Kubernetes, but new to data governance.
> **Requirements:** Use analogies related to IT infrastructure (like Azure Key Vault for secrets or RBAC in Kubernetes) to explain how Unity Catalog manages data access and permissions. Keep it under three paragraphs.

### 💡 The Visible Difference in Output

* **Bad Output:** You get a copy-pasted marketing brochure full of buzzwords like "unified governance," "democratization," and "AI-driven," which doesn't explain how it actually works under the hood.
* **Structured Output:** The LLM bypasses the marketing fluff and speaks your language. It compares Unity Catalog's external locations to mounting persistent volumes in Kubernetes, and its permission model to managing service connections in Azure DevOps, making the concept instantly click.

---

## 3. Writing Infrastructure as Code (Structured Output & Constraints)

### ❌ The Bad Prompt

> Write a pipeline to build and deploy an Azure Function.

### 🎯 The Structured (Good) Prompt

> **Task:** Write an Azure DevOps YAML pipeline to deploy a Python-based Azure Function.
> **Constraints:**
> * The pipeline must run on a self-hosted agent pool named `linux-build-agents`.
> * Include a step to run `pytest` before packaging the function.
> * Use the `AzureFunctionApp@2` task for deployment.
> **Output Format:** Provide **only** the raw YAML code in a code block. Do not include any introductory explanations or alternative methods.
> 
> 

### 💡 The Visible Difference in Output

* **Bad Output:** The LLM generates a pipeline using Microsoft-hosted Windows agents, forgets the testing step, and gives you a generic Node.js template instead of Python.
* **Structured Output:** You get perfectly tailored, copy-pasteable YAML that targets your specific self-hosted infrastructure. You drop it into your repo, and it runs successfully on the first try.

---

## 4. Incident Response and Recovery (Chain-of-Thought)

### ❌ The Bad Prompt

> I accidentally ran rm -rf /* on an Ubuntu machine. How do I fix it?

### 🎯 The Structured (Good) Prompt

> **Context:** I accidentally executed `rm -rf /*` on an Ubuntu server. Crucially, I ran this **without sudo**, and I managed to cancel the command via `Ctrl+C` after a few seconds. My home directory is severely affected, but system binaries seem intact.
> **Task:** Provide a recovery plan.
> **Let's think step-by-step:**
> 1. Assess what directories a non-root user actually has permission to delete.
> 2. List the immediate commands I should run to verify the integrity of the system (e.g., checking if `/bin` or `/etc` were touched).
> 3. Provide the steps to rebuild a standard user's home directory (e.g., copying default profiles from `/etc/skel`).
> 
> 

### 💡 The Visible Difference in Output

* **Bad Output:** The LLM panics, assumes the entire OS is destroyed, and tells you to immediately format the drive, reinstall Ubuntu, and restore from backups—causing unnecessary downtime.
* **Structured Output:** By forcing the model to evaluate the "without sudo" constraint step-by-step, it logically concludes that the root filesystem is completely safe. It skips the reinstall advice entirely and focuses exactly on what broke: copying `.bashrc` and `.profile` back into your home directory to restore your user environment.

---

## 5. Exploring New Tech Stacks (Few-Shot & Context)

### ❌ The Bad Prompt

> How do I use RAG with Python?

### 🎯 The Structured (Good) Prompt

> I want to build a simple Retrieval-Augmented Generation (RAG) pipeline in Python. I prefer lightweight, modular frameworks rather than heavy, opinionated ones.
> **Here is an example of what I consider a good recommendation:**
> * *Instead of recommending full-stack Django for a simple API, recommend FastAPI because it is lightweight, fast, and easy to debug.*
> 
> 
> **Task:** Based on this preference for lightweight tools, recommend 2 Python libraries for building a RAG pipeline (e.g., for document parsing, vector storage, or LLM orchestration). Briefly explain *why* they fit this lightweight philosophy.

### 💡 The Visible Difference in Output

* **Bad Output:** The model recommends massive, complex enterprise frameworks, giving you a 50-step tutorial on deploying a heavy vector database cluster that takes three days to configure.
* **Structured Output:** The model understands your design philosophy (thanks to the few-shot example) and recommends lean, highly focused tools (like ChromaDB for local vector storage or a lightweight orchestration script) that you can spin up and test in an afternoon.


## Context Engineering
- Used Typically in AI agents.
- As agent calls LLMs multiple times (aka Turns)
- Bad context will degrade Agents performance
- [Tweet of Master Karpthy](https://x.com/karpathy/status/1937902205765607626?lang=en)
<img width="625" height="806" alt="image" src="https://github.com/user-attachments/assets/5c44239b-c504-47d6-9169-9d7f2b038fa7" />

- [Antropic Guide on Context Engieering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
### [Langchain Docs on context Engineering](https://www.langchain.com/blog/context-engineering-for-agents) || [Principles of context Engineering](https://cognition.ai/blog/dont-build-multi-agents)
## Problems with Long Context
[Source](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)
Context Fails
- Context Poisoning: When a hallucination makes it into the context
- Context Distraction: When the context overwhelms the training
- Context Confusion: When superfluous context influences the response
- Context Clash: When parts of the context disagree
