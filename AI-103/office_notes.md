## Azure AI Foundry & Agent Essentials

* **Prerequisites for Foundry Routines:** Requires an Agent, a Content Analyzer, and Azure AI Search.
* **Hosting an Agent:** Bring your own code (BYOC) directly in Foundry.
* **Model Routing:** Dynamic routing or cascading between different models is natively achieved through the **Model Router** feature in Microsoft Azure AI Foundry.
* **Power Fx Notice:** Microsoft is retiring Foundry workflows on **December 1, 2026**, and recommends the **Microsoft Agent Framework** for new builds.
* **MCP Servers Catalog:** Explore available Model Context Protocol (MCP) servers in the [Microsoft Foundry Tool Catalog](https://ai.azure.com/catalog/tools?search=language).

---

## Content Understanding & Document Processing

The [Content Understanding Studio](https://contentunderstanding.ai.azure.com/) helps analyze any kind of data using custom or prebuilt analyzers. View the [Content Understanding Framework Diagram](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/media/overview/content-understanding-framework-2025.png) for architectural insights.

### Data Encoding Essentials

* **UTF-8:** Encodes text and characters (e.g., `A`, `é`, `你`) into bytes.
* **Base64:** Encodes binary data (bytes) into standard text characters (`A-Z`, `a-z`, `0-9`, etc.).
* **Purpose:** Ensures different systems can consistently understand, store, and transmit data. Encoding is reversible via decoding.
* **Standard Data Flow:** `Binary image -> Base64 text -> JSON request -> API -> decode Base64 -> Images`. API requests are sent as JSON.

### Content Understanding Analyzers

| Analyzer Type | Target Goal & Best Use Case |
| --- | --- |
| **Document Layout Analyzer** | Document structure: reading order, paragraphs, sections, tables, figures. Ideal for RAG, search, and complex PDFs. |
| **Invoice Analyzer** | Specifically for invoices, utility bills, and sales orders to extract vendor, totals, dates, and line items. |
| **Call Center Analyzer** | Analyzing audio and call-center conversations (transcripts, summaries, sentiment, and classification). |
| **Tax (US) Analyzer** | Prebuilt analyzers specifically for US tax forms (Form 1040 and schedules). |
| **OCR Read Analyzer** | General text recognition/OCR when layout-aware extraction isn't specifically required. |
| **Document Fields Analyzer** | Extracting custom-defined fields (e.g., contract party, renewal date, policy number). |

### Schema Creation & Cost Optimization Workflow

1. **Studio Setup:** Go to the Content Understanding Studio (requires a Blob Storage account, Foundry, and chat completion model).
2. **Configuration Methods:**
* **Extract:** Find specific values in the document.
* **Classify:** Categorize or label (requires predefined categories/enums, such as `SSlip` vs. `Others`).
* **Generate:** Have the model synthesize or create content.
* **Auto:** Let Content Understanding determine the best approach.


3. **Cost Reduction Tip:** Processing full multi-page documents through large models can incur high token costs. To optimize:
* Deploy a lightweight mini-classifier first to determine document type.
* Provide detailed field descriptions to act as mini-prompts, reducing false extractions.



---

## Azure Speech SDK & Configurations

`SpeechConfig` handles service authentication and behavior (language, voice, output format), while `AudioConfig` defines input sources, and `AudioOutputConfig` specifies synthesis destinations.

### Azure Speech Configuration Matrix

| Scenario | Config Object | Runtime Object | Audio Config |
| --- | --- | --- | --- |
| **Speech to Text (STT)** | `SpeechConfig` | `SpeechRecognizer` | `AudioConfig` (optional) |
| **Text to Speech (TTS)** | `SpeechConfig` | `SpeechSynthesizer` | `AudioOutputConfig` (optional) |
| **Speech to Speech** | `SpeechConfig` + App/LLM logic | Recognizer + Synthesizer | Input + Output |
| **Speech to Translation Text** | `SpeechTranslationConfig` | `TranslationRecognizer` | `AudioConfig` |
| **Speech to Translation Speech** | `SpeechTranslationConfig` | `TranslationRecognizer` | Input / Output as required |
| **Continuous Transcription** | `SpeechConfig` | `SpeechRecognizer` | `AudioConfig` |
| **Conversation Transcription** | `SpeechConfig` | `ConversationTranscriber` | `AudioConfig` |
| **Multichannel Transcription** | `SpeechConfig` | `SpeechRecognizer` | File / Stream `AudioConfig` |
| **Azure OpenAI Speech Pipeline** | `SpeechConfig` + Azure OpenAI Client | Recognizer + OpenAI + Synthesizer | Input + Output |

### Key Speech Concepts

* **Diarization:** Azure AI Speech automatically separates and labels different speakers in a recording with generic IDs (e.g., `Guest-1`, `Guest-2`).
* **Custom Model Lifecycle:** When an expired custom speech model endpoint is reached, Azure falls back to the most recent base model for service continuity (though batch transcription requests fail with a `4xx` error).
* **SSML (Speech Synthesis Markup Language):** An XML-based markup language giving developers precise control over pacing, volume, pitch, speed, and emotional style for TTS engines.

---

## Azure Language, Search & Content Safety

### Azure Language Service

* Cloud-based NLP service available directly or via the Azure Language MCP server (remote catalog or local environment).
* **Custom Named Entity Recognition (CNER):** Build custom models to extract domain-specific entity categories from unstructured text (requires a storage account).
* **Conversational Language Understanding (CLU):** Predict overall user intent and extract key slot information.
* **PII Redaction:** Detect, classify, and redact sensitive personal identifiable information across text and transcripts.

### Azure AI Search

* **Core Components:** Replicas, Partitions, Indexes, Indexers, Search Units, Vector Quotas, and allowed data sources.
* **Field Properties:** Retrievable, Filterable, Sortable, Facetable, and Searchable.
* **Key Features:** Semantic Ranker, AI Enrichments, and `@odata.count` response indicators.

### AI Content Safety

Machine learning-assisted moderation APIs to detect potentially offensive, risky, or undesirable material in user- and AI-generated text and images.

* **Prompt Shields:** Protects against indirect/hidden prompt injections in documents and images.
* **Groundedness Detection:** Verifies response fidelity.
* **Protected Material Detection:** Identifies copyrighted content and sources.

---

## Diagnostic Logging & Observability

Enable diagnostic settings via the Azure Portal under your Foundry resource by routing to a Log Analytics Workspace, Storage Account, or Event Hub.

### Diagnostic Log Categories

| Category | Purpose / Data Captured | Destination Options |
| --- | --- | --- |
| **Audit Logs** | Security events, resource lifecycle, permission changes. | Log Analytics, Storage Account, Event Hubs |
| **Request & Response Logs** | API request/response metadata, status codes, latency. | Log Analytics, Storage Account, Event Hubs |
| **Azure OpenAI Request Usage** | Token counts, model consumption metrics. | Log Analytics, Storage Account, Event Hubs |
| **AllMetrics** | Resource-level and system metrics (error rates, counts). | Azure Monitor Metrics / Log Analytics |

* **Tracing:** Shows ordered span sequences of LLM calls, tool invocations, and timing within a single run to diagnose latency and correctness issues. Connect **Application Insights** to your project for server-side tracing.

---
# MS DOCS:

### Foundry SDK:
> Create a project in West US 3 try an instant model (preview).
```py
pip install "azure-ai-projects>=2.3.0" azure-identity
project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Run a responses API call
response = openai.responses.create(
    model="gpt-5-mini",  # supports all Foundry direct models
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")
```
- Foundry Agent = Model + System Instructions + Tools. Benefit: it ensures consistent responses in user interactions without repeating instructions each time

```py
agent = project.agents.create_version(
    agent_name=FOUNDRY_AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-5-mini",  # supports all Foundry direct models
        instructions="You are a helpful assistant that answers general questions",
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```
- Once u got agent, chat with it

```py
openai = project.get_openai_client(agent_name=FOUNDRY_AGENT_NAME) =========

# Create a conversation for multi-turn chat
conversation = openai.conversations.create() ==========***

# Chat with the agent to answer questions
response = openai.responses.create(
    conversation=conversation.id,  ==========***
    input="What is the size of France in square miles?",
)
print(response.output_text)

# Ask a follow-up question in the same conversation
response = openai.responses.create(
    conversation=conversation.id,  ==========***
    input="And what is the capital city?",
)
print(response.output_text)
```

### Agent types: 
✅ `pip install -U` The -U (or --upgrade) flag in the pip install command instructs pip to upgrade the specified packages to the newest available version.
> You can start declarative (Prompt Agent) and move to code as your needs grow. Foundry Project Manager at project scope. If you need to create a new Foundry project, you need the Owner role at resource group scope.
1. **Prompt Agent**:
- created via foundry portal or sdk
- foundry hosts and runs them
- no app code or compute to maintain
2. **Hosted agent**:
  - Bring your code ( Microsoft Agent Framework, LangGraph, or Semantic Kernel)
  - Foundry runs it with a managed endpoint, scaling, identity, and observability
  - https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd
  - **MS Agent Framework**: `pip install -U agent-framework agent-framework-foundry-hosting azure-identity python-dotenv`
  - `ResponsesHostServer` for the OpenAI-compatible /responses endpoint.
`InvocationsHostServer` for the generic /invocations endpoint.
