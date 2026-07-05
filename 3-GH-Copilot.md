## Availability
- About GitHub Copilot code review
Copilot reviews your pull requests, identifies issues, and suggests fixes you can apply in a couple of clicks.

- Who can use this feature?
**Available for all paid Copilot plans.**
[Pricing](https://github.com/features/copilot/plans?ref_product=copilot&ref_type=purchase&ref_style=text&ref_plan=cfi)
- available in VS Code, Github.com, Azure DevOps
-  Copilot Free plan, which does not include Copilot code review.
- If Using GH Enterprise then Pay as Go but have to enable setting at Org Level - [docs](https://docs.github.com/en/copilot/concepts/agents/code-review)

## Capa
Copilot code review uses GitHub Actions to run the agentic capabilities, including full project context gathering and passing suggestions to Copilot cloud agent. By default, Copilot code review uses standard GitHub-hosted runners. You can also upgrade to larger GitHub-hosted runners for better performance, or use self-hosted runners.

GH AI Credits  = Model Used and Number of Tokens used 
- If a repository is configured to automatically request a code review from Copilot for all new pull requests, the AI credits consumption is attributed to the pull request author

## How 
-  repository includes agent skills, Copilot code review can automatically use relevant skills when reviewing a pull request, extending Copilot beyond its built-in analysis.
> GH docs says: Copilot is not guaranteed to spot all problems or issues in a pull request. Sometimes it will make mistakes. Always validate Copilot's feedback carefully. Supplement Copilot's feedback with a human review.
