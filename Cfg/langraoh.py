import os
import logging
import asyncio
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Azure OpenAI imports
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

# MCP imports
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

# -----------------------------
# 1. Setup Logging & Env
# -----------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")

# -----------------------------
# 2. Initialize Azure credentials
# -----------------------------
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# -----------------------------
# 3. MCP Server Setup
# -----------------------------
server_params = StdioServerParameters(
    command="C:\Tool\node\npx.cmd",
    args=["-y", "@azure/mcp@latest", "server", "start"],
    env=None
)

# -----------------------------
# 4. LangGraph State
# -----------------------------
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# -----------------------------
# 5. Chat Node with MCP integration
# -----------------------------
async def chat_node(state: ChatState, session: ClientSession, client: AzureOpenAI) -> ChatState:
    last_msg = state["messages"][-1].content if state["messages"] else ""
    
    # Simple MCP server status
    server_status = "Azure MCP Server: Available ✅"

    # Detect pricing questions
    if any(word in last_msg.lower() for word in ["price", "cost", "pricing"]):
        # Pick first tool for pricing
        tools = await session.list_tools()
        pricing_tool = next((t for t in tools.tools if "pricing" in t.name.lower()), None)
        if pricing_tool:
            try:
                # Call MCP pricing tool
                tool_args = {"query": last_msg}
                result = await session.call_tool(pricing_tool.name, tool_args)
                return {"messages": [SystemMessage(content=f"{server_status}\n{result.content}")]}

            except Exception as e:
                return {"messages": [SystemMessage(content=f"{server_status}\nError calling tool: {e}")]}

    # Otherwise, normal Azure OpenAI response
    messages_for_model = state["messages"] + [
        SystemMessage(content=f"MCP Server Status:\n{server_status}")
    ]

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL,
        messages=[{"role": m.role, "content": m.content} for m in messages_for_model]
    )
    return {"messages": [SystemMessage(content=response.choices[0].message.content)]}

# -----------------------------
# 6. Main async loop
# -----------------------------
async def main():
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version="2024-04-01-preview",
        azure_ad_token_provider=token_provider
    )

    # Start MCP client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List MCP tools
            tools = await session.list_tools()
            print("🔹 MCP Server Connected")
            for t in tools.tools:
                print(f" - {t.name} (description: {t.description})")
            print("\n🔹 Ready to chat! Type 'exit' to quit.\n")

            # Build LangGraph workflow
            workflow = StateGraph(ChatState)
            workflow.set_entry_point("chat")
            
            async def node_wrapper(state):
                return await chat_node(state, session, client)

            workflow.add_node("chat", node_wrapper)
            workflow.add_edge("chat", END)
            chatbot = workflow.compile()

            # Chat loop
            history = [SystemMessage(content="You are a helpful assistant with Azure MCP pricing access.")]
            while True:
                user_input = input("You: ")
                if user_input.lower() in {"exit", "quit"}:
                    break

                history.append(HumanMessage(content=user_input))
                output = await chatbot.invoke({"messages": history})
                ai_response = output["messages"][-1]
                history.append(ai_response)

                print(f"Bot (Azure MCP Server): {ai_response.content}\n")

# -----------------------------
# 7. Run
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
