import asyncio
from fastmcp import Client

# # In-memory server (running locally - ideal for testing)
# server = FastMCP("AzureTestServer")
# client = Client(server)

# HTTP server
client = Client("https://learn.microsoft.com/api/mcp")

async def main():
    async with client:
        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        print(f"TOOLS:\n {tools}")
        print('='*50)
        print(f"RESOURCES:\n {resources}")
        print('='*50)
        print(f"PROMPTS:\n {prompts}")
        print('='*50)
        print("Below is the list of Tools exposed to LLM: ")
        for item in tools:
            print(f"Name: {item.name}")
            #print(f"Description: {item.description}")

        # Execute operations
        # result = await client.call_tool("example_tool", {"param": "value"})
        # print(result)

asyncio.run(main())