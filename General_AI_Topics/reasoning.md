### Notes
[MS Docs](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning?tabs=csharp%2Cgpt-6)
- Easy task → fast thinking → quick answer
- Hard task → deeper thinking → potentially better answer, but more time/compute
- Azure OpenAI reasoning models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

Key capabilities of reasoning models:

1. Complex Code Generation: Capable of generating algorithms and handling advanced coding tasks to support developers.
2. Advanced Problem Solving: Ideal for comprehensive brainstorming sessions and addressing multifaceted challenges.
3. Complex Document Comparison: Perfect for analyzing contracts, case files, or legal documents to identify subtle differences.
4. Instruction Following and Workflow Management: Particularly effective for managing workflows requiring shorter contexts.
> Reasoning models generate reasoning tokens in addition to the input and output tokens you're already familiar with. The model uses those tokens to work through your prompt: breaking the problem apart, weighing approaches, and abandoning paths that don't hold up. Reasoning tokens never appear in the message content, but they occupy space in the context window and are billed as output tokens.
`output_tokens_details.reasoning_tokens in a Responses API response` : **Reasoning tokens are billed as output tokens, so a request that thinks longer costs more even when the visible answer is short. To cap the total the model generates, set max_output_tokens**

#### reasoning modes
Persisted reasoning is about continuity, not transparency. The reasoning items stay opaque, and the API never returns their reasoning text. Set reasoning.context to control which of the available reasoning items the model can draw on.
![](https://learn.microsoft.com/en-us/azure/foundry/openai/media/how-to/reasoning/reasoning-context-modes.svg)

- In code: The `reasoning_effort parameter` controls how much the model thinks before it answers. Supported values vary by model and include none, minimal, low, medium, high, xhigh, and max. Defaults vary by model as well. For the values each model accepts, see API and feature support.
- ```py
  second = client.responses.create(
    model="gpt-5.6",
    previous_response_id=first.id,
    input="Now patch the bug and explain the change.",
    reasoning={"context": "all_turns"},
)
```
