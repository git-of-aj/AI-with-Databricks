1152f2fa3c1ef773546e561f75eaaecc20d8eda3c2ec8fa926fe2831da7085ef
https://techcommunity.microsoft.com/blog/educatordeveloperblog/cicd-for-ai-agents-on-microsoft-foundry/4522218

agent.yaml: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-yaml-reference

GOAT Agent Monitoring: https://microsoft.github.io/ai-agents-for-beginners/10-ai-agents-production/

secure, scalable ci-cd for app and AI workloads                                                                               today: CI-CD + DevSecOps + AI Agent CI-CD
                                                                   - Azure Pipeline documentations (focus on re-usebl
                                                                   - GH-300
                                                                   - DevSecOps - Veeramalla
                                                                   - Blogs on CI-CD AI 
https://devblogs.microsoft.com/devops/
                                                                   tomor: TF Associate + Ansible 
                                                                    Docker & K8s
                                                                   thurs: Docker & k8s & linux & Python
foundry based solutions
tf and ansible / ARM/ Bicep
docker k8s [AKS,APP SERVICE,FUNCTIONS]
linux / Windows
Azure devops,GH actions and Jenkins
Azure / AWS
Strong scipting - python, bash
DevSecOps: sonar, checkmarx, fortify, codeacy
Polaris, nexus, nessus
MLOps
Model Lifecycle 

we’ve encouraged customers to move their repositories from Azure Repos to GitHub, 
Copilot Autofix is available today in limited private preview
Autofix closes that gap. It uses the same CodeQL engine that finds a vulnerability to generate an AI-suggested fix for it, right in the Azure DevOps alert experience. You review the suggested change, edit it if you need to, and then commit it to a pull request without leaving the alert.
- Ruff Lint: linter, like Ruff, is a tool that analyzes your code and looks for errors, stylistic issues, and suspicious constructs.
- Bandit is an open-source Static Application Security Testing (SAST) tool explicitly designed to find common security flaws in Python code
- Write small unit tests - python
- 
Observability tools such as Langfuse or Microsoft Foundry usually represent agent runs as traces and spans.
Trace represents a complete agent task from start to finish (like handling a user query).
Spans are individual steps within the trace (like calling a language model or retrieving data).

Without observability, an AI agent can feel like a “black box” - its internal state and reasoning are opaque, making it difficult to diagnose issues or optimize performance. With observability, agents become “glass boxes,” offering transparency that is vital for building trust and ensuring they operate as intended.
- Test cases (evals for llm):  QnA pair ==> small sets of questions for quick checks and larger ones for broader performance metrics​.

the deployable artifact = ZAR/WAR/ file or container tag in AI Agent its version = Model selection + Tools + system instruction + artifacts
P95 (95th percentile) latency is the response time threshold under which 95% of your requests complete. If your P95 is 400 ms, it means 95 out of every 100 requests finish in 400 ms or less, while the slowest 5% of requests take longer

Option        Structure        Best for        Trade-off
A — Recommended        Dev Project → Test Project → Prod Project (separate Foundry projects)        Enterprise workloads        Full isolation, clean RBAC boundaries, easier governance
B — Lightweight        Single Foundry project with agent version tags (dev/test/prod)        Small teams, prototyping        Simpler setup, but weaker environment separation
