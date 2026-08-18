import os

from dotenv import load_dotenv
from azure.identity import AzureCliCredential

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.ai.agentserver.invocations import InvocationAgentServerHost

from starlette.requests import Request
from starlette.responses import JSONResponse


load_dotenv()


# --------------------------------------------------
# 1. Connect to Microsoft Foundry
# --------------------------------------------------

client = FoundryChatClient(
    project_endpoint=os.getenv("ENDPOINT"),
    model=os.getenv("MODEL"),
    credential=AzureCliCredential(),
)


# --------------------------------------------------
# 2. Create your agent
# --------------------------------------------------

agent = Agent(
    client=client,
    name="ConversationAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
)


# --------------------------------------------------
# 3. Create the Invocation Agent Server
# --------------------------------------------------

app = InvocationAgentServerHost()


# --------------------------------------------------
# 4. Handle Foundry invocations
# --------------------------------------------------

@app.invoke_handler
async def handle_invocation(request: Request):

    # Read incoming request
    data = await request.json()

    # Get the user's message
    query = data.get("message")

    if not query:
        return JSONResponse(
            {"error": "message is required"},
            status_code=400,
        )

    # Run your Foundry agent
    result = await agent.run(query)

    # Return the agent response
    return JSONResponse({
        "response": str(result)
    })


# --------------------------------------------------
# 5. Start the server
# --------------------------------------------------

if __name__ == "__main__":
    app.run()
