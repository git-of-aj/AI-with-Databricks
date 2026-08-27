# uv pip install agent-framework agent-framework-foundry python-dotenv azure-identity
# Trainer-AJ Github Account => MCP Fine grained token name
# Prompt: 
# summarize about topic: using hosted mcp tools in Microsoft agent framework, put that in a readme.md file,
#  then create a new repo in my GitHub named mcp-2-gh and upload this readme.md there,
#  give back GitHub repo url once all done image under image folder.

import asyncio
import os

from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient


# Load .env
load_dotenv("webapp-under-progress/.env")


async def main() -> None:
    # ---------------------------------------------------------
    # 1. Configuration
    # ---------------------------------------------------------

    github_pat = os.getenv("GITHUB_PAT")

    if not github_pat:
        raise ValueError("GITHUB_PAT environment variable is not set.")

    github_headers = {
        "Authorization": f"Bearer {github_pat}"
    }

    # ---------------------------------------------------------
    # 2. Create Azure credential + Foundry client
    # ---------------------------------------------------------

    async with AzureCliCredential() as credential:

        client = FoundryChatClient(
            project_endpoint=(
                "https://foundry0309.services.ai.azure.com/"
                "api/projects/proj-default"
            ),
            model="gpt-5-mini",
            credential=credential,
        )

        # -----------------------------------------------------
        # 3. Create Microsoft Learn MCP tool
        # -----------------------------------------------------

        print("[startup] Connecting Microsoft Learn MCP...")

        learn_mcp_tool = client.get_mcp_tool(
            name="Microsoft Learn",
            url="https://learn.microsoft.com/api/mcp",
            approval_mode="never_require",
        )

        # -----------------------------------------------------
        # 4. Create GitHub MCP tool
        # -----------------------------------------------------

        print("[startup] Connecting GitHub MCP...")

        github_mcp_tool = client.get_mcp_tool(
            name="GitHub",
            url="https://api.githubcopilot.com/mcp/",
            headers=github_headers,
            approval_mode="never_require",
        )

        # -----------------------------------------------------
        # 5. Create one agent with BOTH MCP servers
        # -----------------------------------------------------

        async with Agent(
            client=client,
            name="MCPAgent",
            instructions=(
    "You are a helpful assistant that can help users interact with GitHub. "
    "The GitHub MCP connection is already authenticated. "
    "Use GitHub MCP for GitHub requests and maintain conversation context. "
    "For 'my' requests, use the authenticated GitHub account without asking for the username. "
    "When the questions asks any technical detail about microsoft products use learn_mcp_tool"
    "Always perform the requested operation and be clear about what you're doing."
),

            tools=[
                learn_mcp_tool,
                github_mcp_tool,
            ],
        ) as agent:

            print("\n========================================")
            print(" MCP Agent is ready")
            print(" Type 'exit' or 'bye' to quit")
            print("========================================\n")

            # -------------------------------------------------
            # 6. Keep accepting queries forever
            # -------------------------------------------------

            while True:

                query = input("You: ").strip()

                if not query:
                    continue

                if query.lower() in ("exit", "bye"):
                    print("Goodbye!")
                    break

                print("\n[agent] Processing your request...")

                print(
                    "[agent] LLM is deciding whether to use "
                    "Microsoft Learn MCP or GitHub MCP..."
                )

                try:
                    # -------------------------------------------------
                    # 7. Stream the response
                    # -------------------------------------------------

                    print("\nAssistant: ", end="", flush=True)

                    stream = agent.run(
                        query,
                        stream=True,
                    )

                    async for update in stream:

                        # Show streamed text immediately
                        if update.text:
                            print(
                                update.text,
                                end="",
                                flush=True,
                            )

                    print("\n")

                    print("[agent] Response complete.\n")

                except Exception as e:
                    print(f"\n[error] {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
