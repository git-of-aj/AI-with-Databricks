## Intro 
> In MCT Subscription use - gpt-5.4-mini, even gpt-5 doesn't support skill

- Skills are versioned bundles of files that you can reuse across shell environments in the Responses API. Use skills to codify processes and conventions—anything from a company style guide to a multi-step workflow—and make them available to the model when it runs the shell tool.
- [Link](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/skills?tabs=python)
- Treat Skills as privileged instructions/code, not harmless documentation. Microsoft explicitly warns that Skills can influence planning, tool usage, and command execution, and recommends reviewing them and controlling which Skills users can invoke. 
### How to 
- Shell = hands
- Skill = procedure / playbook

Create a skill
Upload a skill bundle in either of these formats:

## First step: Upload skill then refer it in shell 
1. Directory upload (multipart): Upload multiple files. Each part includes the file path relative to a single top-level folder.
2. Zip upload: Zip a single top-level folder and upload the .zip file.
- The zip package must include `SKILL.md at its root`.
The upload returns a skill_id that you reference when you attach the skill to a shell environment.

`OR`
- Use MS skill catalogue of pre-build skills
- Github Repo of All MS Skill : https://github.com/microsoft/skills 


