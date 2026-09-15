## Memory Types [Ref: Neo4j](https://neo4j.com/labs/agent-memory/explanation/memory-types/)
Each memory type has a different lifecycle:

- Short-term: Active during conversation, may be summarized after
- Long-term: Persists indefinitely, grows over time
- Reasoning: Archival - useful for analysis and pattern learning

**Different Access Patterns**
Each type is queried differently:

- Short-term: "What did we just discuss?" → Recent messages in sequence
- Long-term: "What do I know about X?" → Graph traversal and semantic search
- Reasoning: "How did I solve similar problems?" → Trace similarity search

**Different Schemas**
Each type has different structure:
- Short-term: Linear sequences of messages
- Long-term: Graph of typed entities with relationships
- Reasoning: Trees of traces → steps → tool calls

## Basics
> An LLM itself is entirely stateless, while a conversation is a growing sequence of text that your application feeds back into the model to simulate memory
- Conversation = the ongoing chat/history. A conversation is the continuing sequence of messages between the user and the AI.
eg:
```txt
User: "Help me plan a dinner."
AI: "Sure. What cuisine do you prefer?"
User: "Italian."
```
- State = (state = RAG + TOOL CALL + User INPUT + OTHER INFO ) what is happening in the current interaction. State is usually short-lived and related to the current workflow.
- Session memory = facts you deliberately remember about the user. Session memory is information you intentionally store about a user so it can be retrieved later and used in a different conversation/session.
- Context = the information you actually give the model for this particular answer
## tool call
- The tool call/result can be part of the ongoing response/conversation state, allowing subsequent turns to continue with the relevant interaction history.
- Tool execution produces data. The application/model can use that data as part of the current response processing and conversation state.
But don't confuse that with:
"The model has permanently learned/stored the result."
It hasn't.
