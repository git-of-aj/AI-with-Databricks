The `ai_chat.py` file:
```
User
  ↓
OpenAI Responses API
  ↓
Model selects GitHub MCP
  ↓
GitHub MCP approval request
  ↓
YOUR PROGRAM
  ↓
prints empty output_text
  ↓
DONE ❌
```

- Problem:  We get empty response 
- logs says:
```
Ask a question: use github tool and list me all github repo
[2026-08-13T17:44:16.103+05:30] [INFO] User request received.
[2026-08-13T17:44:16.104+05:30] [INFO] Request #3 input:
[2026-08-13T17:44:16.105+05:30] [INFO]   use github tool and list me all github repo
[2026-08-13T17:44:16.106+05:30] [INFO] Building Responses API request...
[2026-08-13T17:44:16.106+05:30] [INFO] Tools configured:
[2026-08-13T17:44:16.108+05:30] [INFO]   - GitHub MCP
[2026-08-13T17:44:16.109+05:30] [INFO]   - Web search
[2026-08-13T17:44:16.111+05:30] [INFO] MCP approval mode: ALWAYS
[2026-08-13T17:44:16.114+05:30] [INFO] Sending request to OpenAI/Azure Responses API...
[2026-08-13T17:44:16.116+05:30] [INFO] STATUS: WAITING_FOR_OPENAI_RESPONSE
[2026-08-13T17:44:21.047+05:30] [INFO] OpenAI/Azure Responses API returned after 4.929 seconds.
[2026-08-13T17:44:21.048+05:30] [INFO] STATUS: OPENAI_RESPONSE_RECEIVED
[2026-08-13T17:44:21.049+05:30] [INFO] Response ID: resp_04d5988305b89394006a7db51946ec81979ea1e4dea01f7e00
[2026-08-13T17:44:21.049+05:30] [INFO] Response model: gpt-4.1
[2026-08-13T17:44:21.050+05:30] [INFO] Response status: completed
[2026-08-13T17:44:21.052+05:30] [INFO] Number of output items: 2
[2026-08-13T17:44:21.053+05:30] [INFO] OUTPUT ITEM #1
[2026-08-13T17:44:21.054+05:30] [INFO] Type: mcp_list_tools
[2026-08-13T17:44:21.058+05:30] [INFO] MCP-related output detected.
[2026-08-13T17:44:21.059+05:30] [INFO] MCP output type: mcp_list_tools
[2026-08-13T17:44:21.061+05:30] [INFO] MCP id: mcpl_04d5988305b89394006a7db51968ec819790c81d875dff2626
[2026-08-13T17:44:21.062+05:30] [INFO] MCP server_label: github
[2026-08-13T17:44:21.063+05:30] [INFO] OUTPUT ITEM #2
[2026-08-13T17:44:21.064+05:30] [INFO] Type: mcp_approval_request
[2026-08-13T17:44:21.067+05:30] [INFO] MCP-related output detected.
[2026-08-13T17:44:21.067+05:30] [INFO] MCP output type: mcp_approval_request
[2026-08-13T17:44:21.068+05:30] [INFO] MCP id: mcpr_04d5988305b89394006a7db51c049c8197856d3f02f756a5f1
[2026-08-13T17:44:21.069+05:30] [INFO] MCP name: search_repositories
[2026-08-13T17:44:21.070+05:30] [INFO] MCP server_label: github
[2026-08-13T17:44:21.070+05:30] [INFO] MCP arguments: {"query":"","minimal_output":true,"order":"asc","page":1,"perPage":10,"sort":"stars"}
[2026-08-13T17:44:21.071+05:30] [INFO] STATUS: MCP_APPROVAL_REQUIRED
[2026-08-13T17:44:21.072+05:30] [INFO] The model/server has requested MCP approval.
[2026-08-13T17:44:21.073+05:30] [INFO] The current program does NOT automatically approve this request.
[2026-08-13T17:44:21.074+05:30] [INFO] Final response text:
[2026-08-13T17:44:21.075+05:30] [INFO] 
[2026-08-13T17:44:21.076+05:30] [INFO] Input tokens: 8797
[2026-08-13T17:44:21.077+05:30] [INFO] Output tokens: 38
[2026-08-13T17:44:21.078+05:30] [INFO] Total tokens: 8835
[2026-08-13T17:44:21.081+05:30] [INFO] STATUS: REQUEST_COMPLETED
[2026-08-13T17:44:21.082+05:30] [INFO] Total request time: 4.979 seconds

================================================================================

================================================================================

ID: resp_04d5988305b89394006a7db51946ec81979ea1e4dea01f7e00
Model: gpt-4.1
Input Tokens: 8797
Output Tokens: 38
Total Tokens: 8835

Request completed in 4.98s

```
- solution:
```txt
User
  ↓
OpenAI
  ↓
mcp_approval_request
  ↓
YOUR PROGRAM detects it
  ↓
YOUR PROGRAM approves it
  ↓
OpenAI Responses API continuation
  ↓
GitHub MCP
  ↓
GitHub result
  ↓
OpenAI
  ↓
final answer
```

- suggested require_approval: "always" as a debugging mode, but I didn't give you the required continuation loop. That's why your current test stops exactly where your logs show it does
- current working code:
```txt
User query
   ↓
OpenAI Responses API
   ↓
ALL MCP servers
   ├── Microsoft Learn → discover all tools
   ├── GitHub          → discover all tools
   └── Web Search
```
- Hybrid Router
```txt
                User query
                    │
                    ▼
             Rule-based check
                    │
        ┌───────────┴───────────┐
        │                       │
   obvious match           ambiguous
        │                       │
        ▼                       ▼
   direct route            LLM router
                                │
                                ▼
                         selected server
```
- The 9,522 tokens are almost certainly coming from the prompt + tool definitions/MCP discovery context, not from the tiny "hi".
