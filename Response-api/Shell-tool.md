## Types: 
- Hosted shell: Azure OpenAI provisions and manages a sandboxed container for the request.
- it's purely disconnected from internet 
- Local shell: You execute the model's shell_call actions in your own runtime and return the results.
- Running arbitrary shell commands can be dangerous. Always sandbox execution, apply allow lists or block lists where possible, and log tool activity for auditing.
- Set the environment to container_auto to let Azure OpenAI provision and manage a container for the request. The model decides whether to call the tool based on your prompt.
- Link: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/shells?tabs=python
- Inline skills are useful when you want a skill to live only for the duration of a single container's lifecycle.
