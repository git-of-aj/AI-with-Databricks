### Where to Host AI Agents
[MS Docs](https://learn.microsoft.com/en-us/agent-framework/hosting/)
- https://learn.microsoft.com/en-us/agent-framework/get-started/hosting?pivots=programming-language-python#hosting-options

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