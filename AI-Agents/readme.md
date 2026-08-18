### Where to Host AI Agents
[MS Docs](https://learn.microsoft.com/en-us/agent-framework/hosting/)
- https://learn.microsoft.com/en-us/agent-framework/get-started/hosting?pivots=programming-language-python#hosting-options
- `InvocationAgentServerHost` — think of it as a specialized FastAPI-like server for agent hosting.
[docs](https://learn.microsoft.com/en-us/python/api/azure-ai-agentserver-invocations/azure.ai.agentserver.invocations.invocationagentserverhost?view=azure-python)
- you create a server host, register an async Python function with @app.invoke_handler, and put your agent logic inside that function. The SDK exposes the invocation endpoint as POST /invocations.

##### Like Foundry Agent `Publish` Option
```txt
Your website / app
       │
       │ HTTPS request
       ▼
Your backend API
       │
       │ Python SDK
       ▼
Azure AI Foundry Agent
       │
       ├── Your instructions
       ├── Tools
       ├── Knowledge / files
       └── Model
```

- Foundry Sample code has `isolation key`
> The isolation key is related to how sessions are isolated. For a multi-user application, you should design the session lifecycle around your users/conversations rather than treating the entire application as one conversation.

For example, conceptually:
`isolation_key = f"user-{user_id}"`
or another appropriate application-specific isolation strategy

### How will my agent communicate ?
```txt
                         ┌───────────────┐
                         │   Your Agent  │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
        MCP: Agent →       A2A: Agent →       AG-UI: Agent →
        tools/context      other agents       user/application

             HUMAN
               ▲
               │
             AG-UI
               │
               ▼
            AGENT
           /     \
        MCP       A2A
        /           \
       ▼             ▼
   TOOLS/DATA    OTHER AGENTS

┌──────────────────────────────────────────────┐
│                  USER                        │
└─────────────────────┬────────────────────────┘
                      │
                    AG-UI
                      │
                      ▼
┌──────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT              │
│                                              │
│   "I need to accomplish this whole task."    │
└───────────────┬──────────────────┬───────────┘
                │                  │
              MCP                 A2A
                │                  │
                ▼                  ▼
        ┌──────────────┐    ┌───────────────┐
        │ Tools / Data │    │ Other Agents  │
        └──────────────┘    └───────┬───────┘
                                    │
                                  MCP
                                    │
                                    ▼
                              Tools / Data

AG-UI at the outside boundary → A2A in the agent ecosystem → MCP at the capability/data layer.
```
These three agentic protocols are complementary and have distinct technical goals; a single agent can and often does use all 3 simultaneously.
#### Agent Harness
- The model is the brain.
- The agent decides what actions to take.
- The harness provides the environment/scaffolding that lets the agent actually work: tools, files, sessions, permissions, context management, planning, etc
- The Harness gives you the agent machinery, but it does NOT tell you what your user interface must look like.
- But it doesn't say: "Your app must have a chat window with a Send button." You can put the harness behind any interface.
- `Same harness, different applications:`
```txt
                 SAME HARNESS
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   Chat interface   CLI/Terminal   API
        │             │             │
   "What should    $ agent run     POST /task
    I do?"              │             │
        │             │             │
        └─────────────┼─────────────┘
                      ↓
                 Harness Agent

```
- `So is Claude / Codex Harness ?`
```txt
                    ┌─────────────────────────┐
                    │     Claude Desktop      │
                    │        / Codex          │
                    ├─────────────────────────┤
                    │ UI / Conversation       │
                    │ Agent loop               │
                    │ *** Harness / scaffolding **    │
                    │ Tools & permissions      │
                    │ File / computer access   │
                    │ Context & memory         │
                    │ Model                    │
                    └─────────────────────────┘
```

Harness Code: https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/harness/build_your_own_claw


### Do you actually need Durable Functions?
> NO : Coz we using Foundry_agent framework

`Durable Functions orchestration:`
```txt
HTTP starter
      ↓
Durable orchestration
      ↓
Activity 1
      ↓
Activity 2
      ↓
Activity 3
      ↓
final result
```

`Our Code is: `
```txt
HTTP request
      ↓
Agent
      ↓
Foundry
      ↓
response
```

> So a normal HTTP-triggered Function is much simpler.

I'd use Durable Functions only if you eventually need something like:
```txt
User request
     ↓
Start long-running agent workflow
     ↓
Search documents
     ↓
Call agent
     ↓
Call another agent
     ↓
Wait 30 minutes
     ↓
Call external API
     ↓
Process results
     ↓
Generate final answer
```
or parallel work:
```
                    ┌── Agent 1 ──┐
                    │             │
Request ────────────┼── Agent 2 ──┼──→ Aggregate → Response
                    │             │
                    └── Agent 3 ──┘
```
That's where Durable Functions becomes valuable.

15. One more option you should consider
Because you're using Microsoft Agent Framework + Foundry, there's another hosting model worth knowing about: Foundry Hosted Agents.

Microsoft now documents hosting an Agent Framework agent directly as a Foundry hosted agent using InvocationsHostServer. 
M
Microsoft Learn

That architecture looks more like:

Your Agent Framework code
          ↓
Foundry Hosted Agent
          ↓
Microsoft Foundry

rather than:

Your Agent Framework code
          ↓
Azure Function
          ↓
Microsoft Foundry

Whether that is better depends on what you're building.

If your goal is simply:

"I have this Python Agent Framework code and I want an API endpoint I can call from my application."

I'd use Azure Functions HTTP trigger.

If your goal is:

"I want this to become a managed agent inside Microsoft Foundry."

I'd investigate Foundry Hosted Agents instead.

My recommended final architecture for your current code
                         ┌─────────────────────┐
                         │   Your Frontend     │
                         │ React / Python / etc│
                         └──────────┬──────────┘
                                    │
                              POST /api/chat
                                    │
                                    ▼
                    ┌────────────────────────────┐
                    │     Azure Function App     │
                    │                            │
                    │  Python v2                 │
                    │  function_app.py           │
                    │                            │
                    │  @app.route("/chat")       │
                    │          │                 │
                    │          ▼                 │
                    │     Agent Framework        │
                    │          │                 │
                    └──────────┼─────────────────┘
                               │
                    Managed Identity
                               │
                               ▼
                    ┌────────────────────────────┐
                    │     Microsoft Foundry      │
                    │                            │
                    │     FoundryChatClient       │
                    │           ↓                │
                    │      Your model            │
                    └────────────────────────────┘

In short
Don't deploy your current file unchanged. Convert it from a CLI program into an HTTP-triggered Function:

input()

→

req.get_json()

and:

AzureCliCredential()

→

DefaultAzureCredential()

Then put:

ENDPOINT
MODEL

in Azure Function App settings, enable Managed Identity, grant that identity access to your Foundry project, and deploy with func azure functionapp publish.

The Microsoft documentation you linked is useful for understanding the Functions/Durable ecosystem, but you don't need Durable Functions for this particular agent code. 
M
Microsoft Learn

If you tell me whether you're deploying from VS Code, Azure Portal, or Azure CLI, I can give you the exact Azure resource creation + deployment commands for your case.


M
Sources


ChatGPT is AI and can make mistakes.

No file chosenNo file chosenNo file chosen

Chat with ChatGPT
Ask anything

