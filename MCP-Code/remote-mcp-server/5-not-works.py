import asyncio
import os
# =======================================
# https://learn.microsoft.com/en-us/agent-framework/agents/tools/tool-approval?pivots=programming-language-python
# ========================================

from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient


async def handle_approvals(query: str, agent) -> str:
    current_input = query

    while True:
        result = await agent.run(current_input)

        if not result.user_input_requests:
            return result.text

        new_inputs = [query]

        for request in result.user_input_requests:
            if request.function_call is None:
                continue

            print("\nApproval needed")
            print(f"Tool: {request.function_call.name}")
            print(f"Arguments: {request.function_call.arguments}")

            answer = input("Allow this tool call? (y/n): ").strip().lower()
            approved = answer in ("y", "yes")

            new_inputs.append(
                Message(role="assistant", contents=[request])
            )

            new_inputs.append(
                Message(
                    role="user",
                    contents=[
                        request.to_function_approval_response(approved)
                    ],
                )
            )

        current_input = new_inputs


async def main():
    load_dotenv(
        r"C:\Users\Ananay.Ojha\Downloads\AI-with-Databricks"
        r"\MCP-Code\remote-mcp-server\webapp-under-progress\.env"
    )

    github_pat = os.getenv("GITHUB_PAT")
    if not github_pat:
        raise ValueError("GITHUB_PAT is not set")

    auth_headers = {
        "Authorization": f"Bearer {github_pat}"
    }

    async with AzureCliCredential() as credential:

        client = FoundryChatClient(
            project_endpoint="https://foundry0309.services.ai.azure.com/api/projects/proj-default",
            model="gpt-5-mini",
            credential=credential,
        )

        github_mcp_tool = client.get_mcp_tool(
            name="GitHub",
            url="https://api.githubcopilot.com/mcp/",
            headers=auth_headers,
            approval_mode="always_require",
        )

        async with Agent(
            client=client,
            name="GitHubAgent",
            instructions=(
                "You are a helpful GitHub assistant. "
                "Use GitHub tools when needed."
            ),
            tools=github_mcp_tool,
        ) as agent:

            print("GitHub Chat App")
            print("Type 'exit' to quit.\n")

            while True:
                query = input("You: ")

                if query.lower() == "exit":
                    break

                try:
                    answer = await handle_approvals(query, agent)
                    print(f"\nAgent: {answer}\n")
                except Exception as e:
                    print(f"\nError: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
