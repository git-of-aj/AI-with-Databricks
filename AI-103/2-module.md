
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
