import asyncio
import os

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.getenv("ENDPOINT"),
        model=os.getenv("MODEL"),
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    # Create a session to maintain conversation history
    session = agent.create_session()

    while True:
        query = input("User: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not query:
            continue

        result = await agent.run(query, session=session)

        print(f"Agent: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())
