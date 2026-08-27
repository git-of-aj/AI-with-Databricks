import asyncio

from azure.identity.aio import AzureCliCredential
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient


async def main():

    async with AzureCliCredential() as credential:

        client = FoundryChatClient(
            project_endpoint="https://foundry0309.services.ai.azure.com/api/projects/proj-default",
            model="gpt-5-mini",
            credential=credential,
        )

        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn",
            url="https://learn.microsoft.com/api/mcp",
            approval_mode="never_require",
        )

        async with Agent(
            client=client,
            name="AzureDocumentationAgent",
            instructions="""
            You are an expert Microsoft Azure documentation assistant.

            Use the Microsoft Learn MCP tools whenever they are
            relevant to answering the user's question.

            Prefer information retrieved from Microsoft Learn.
            """,
            tools=[learn_mcp],
        ) as agent:

            result = await agent.run(
                "How do I configure managed identity for an Azure Function?"
            )

            print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
