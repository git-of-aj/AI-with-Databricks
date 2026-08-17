import os
import asyncio
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

load_dotenv()

# # If Azure CLI is not already on PATH
# os.environ["PATH"] = (
#     r"C:\Tool\azCLI\bin"
#     + os.pathsep
#     + os.environ.get("PATH", "")
# )

credential = AzureCliCredential()

agent = Agent(
    client=FoundryChatClient(
        project_endpoint=os.getenv("ENDPOINT"),
        model=os.getenv("MODEL"),
        credential=credential,
    ),
    name="HelloAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
)


async def main():
    result = await agent.run("What is the largest city in France?")
    print(f"Agent: {result}")
    # Streaming: receive tokens as they are generated
    print("Agent (streaming): ", end="\n", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
