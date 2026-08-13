from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================
# Environment variables
# ============================================================

ENDPOINT = os.getenv("OPENAI_ENDPOINT")
MODEL = os.getenv("OPENAI_DEPLOYMENT")
API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_MCP_PAT = os.getenv("GITHUB_MCP_PAT")

# ============================================================
# OpenAI client
# ============================================================

client = OpenAI(
    base_url=ENDPOINT,
    api_key=API_KEY,
)

# ============================================================
# MCP servers
# ============================================================

microsoft_learn_mcp = {
    "type": "mcp",
    "server_label": "api-specs",
    "server_url": "https://learn.microsoft.com/api/mcp",
    "require_approval": "always",
    "server_description": (
        "This tool provides access to Microsoft Learn documentation. "
        "Use this tool whenever the user asks questions related to "
        "Microsoft technologies such as Azure, Power Apps, "
        "Windows Server, Microsoft 365, .NET, and other Microsoft technologies."
    ),
}

github_mcp = {
    "type": "mcp",
    "server_label": "github",
    "server_url": "https://api.githubcopilot.com/mcp/",
    "require_approval": "always",
    "server_description" : ("Use this tool for any request related to Github."
                            "If user requests branch or Pull Request creation,Repo details use"
                            "Appropriate tools"
                            "Always use Github Account git-of-aj"
                            ),
    "headers": {
        "Authorization": f"Bearer {GITHUB_MCP_PAT}"
    },
}

web_search = {
    "type": "web_search"
}

# IMPORTANT:
# Keep this same tools list for BOTH the initial request
# and every approval continuation request.

tools = [
    microsoft_learn_mcp,
    github_mcp,
    web_search,
]


# ============================================================
# Process MCP approvals
# ============================================================

def process_mcp_approvals(response):

    while True:

        approval_inputs = []

        for item in response.output:

            if item.type == "mcp_approval_request":

                print("\nMCP approval requested:")
                print(f"  Server: {item.server_label}")
                print(f"  Tool:   {item.name}")

                approval_inputs.append(
                    {
                        "type": "mcp_approval_response",
                        "approve": True,
                        "approval_request_id": item.id,
                    }
                )

        # No more approval requests.
        if not approval_inputs:
            break

        print("Automatically approving MCP request(s)...")

        # IMPORTANT:
        # The tools MUST be supplied again here.
        # Otherwise the MCP server is not enabled for this
        # continuation request.
        response = client.responses.create(
            model=MODEL,
            tools=tools,
            input=approval_inputs,
            previous_response_id=response.id,
        )

    return response


# ============================================================
# Main loop
# ============================================================

print("Type 'exit' or 'quit' to stop\n")

while True:

    user_input = input("Ask a question: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        break

    if not user_input:
        continue

    try:

        # ----------------------------------------------------
        # Initial request
        # ----------------------------------------------------

        response = client.responses.create(
            model=MODEL,
            tools=tools,
            input=user_input,
        )

        # ----------------------------------------------------
        # Process MCP approvals
        # ----------------------------------------------------

        response = process_mcp_approvals(response)

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        print("\n" + "=" * 80)
        print(response.output_text)
        print("=" * 80)

        # ----------------------------------------------------
        # Usage
        # ----------------------------------------------------

        if response.usage:

            usage = response.usage

            print(
                f"\nID: {response.id}\n"
                f"Model: {response.model}\n"
                f"Input Tokens: {usage.input_tokens}\n"
                f"Output Tokens: {usage.output_tokens}\n"
                f"Total Tokens: {usage.total_tokens}\n"
            )

    except Exception as ex:

        print(f"\nError: {ex}\n")
