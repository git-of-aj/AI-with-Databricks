from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess
import logging

load_dotenv()

# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs.txt", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("mcp-client")

# Uncomment these if you want very detailed HTTP logs.
# They can be noisy.
logging.getLogger("openai").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)


def log_stage(message):
    logger.info("=" * 70)
    logger.info(message)
    logger.info("=" * 70)


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

log_stage("STARTING APPLICATION")

logger.info("OpenAI endpoint: %s", ENDPOINT)
logger.info("OpenAI model/deployment: %s", MODEL)
logger.info("API key loaded: %s", bool(API_KEY))
logger.info("GitHub MCP PAT loaded: %s", bool(GITHUB_MCP_PAT))

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
    "server_description": (
        "Use this tool for any request related to Github. "
        "If user requests branch or Pull Request creation, Repo details use "
        "appropriate tools. Always use Github Account git-of-aj."
    ),
    "headers": {
        "Authorization": f"Bearer {GITHUB_MCP_PAT}"
    },
}

web_search = {
    "type": "web_search"
}


# IMPORTANT:
# Same tools list must be supplied to the initial request
# and every approval continuation request.

tools = [
    microsoft_learn_mcp,
    github_mcp,
    web_search,
]


# ============================================================
# Inspect response
# ============================================================

def inspect_response(response):

    logger.info("Response ID: %s", response.id)

    for item in response.output:

        item_type = getattr(item, "type", "unknown")

        # ----------------------------------------------------
        # MCP tool discovery
        # ----------------------------------------------------

        if item_type == "mcp_list_tools":

            server_label = getattr(
                item,
                "server_label",
                "unknown",
            )

            logger.info(
                "MCP DISCOVERY COMPLETE | server=%s",
                server_label,
            )

            discovered_tools = getattr(
                item,
                "tools",
                None,
            )

            if discovered_tools:

                logger.info(
                    "MCP DISCOVERY | %d tools discovered",
                    len(discovered_tools),
                )

                for tool in discovered_tools:

                    tool_name = getattr(
                        tool,
                        "name",
                        str(tool),
                    )

                    logger.info(
                        "MCP TOOL AVAILABLE | %s",
                        tool_name,
                    )

        # ----------------------------------------------------
        # MCP approval
        # ----------------------------------------------------

        elif item_type == "mcp_approval_request":

            server_label = getattr(
                item,
                "server_label",
                "unknown",
            )

            tool_name = getattr(
                item,
                "name",
                "unknown",
            )

            logger.warning(
                "MCP APPROVAL WAITING | server=%s | tool=%s | approval_id=%s",
                server_label,
                tool_name,
                item.id,
            )

        # ----------------------------------------------------
        # MCP execution
        # ----------------------------------------------------

        elif item_type == "mcp_call":

            server_label = getattr(
                item,
                "server_label",
                "unknown",
            )

            tool_name = getattr(
                item,
                "name",
                "unknown",
            )

            status = getattr(
                item,
                "status",
                "unknown",
            )

            logger.info(
                "MCP CALL | server=%s | tool=%s | status=%s",
                server_label,
                tool_name,
                status,
            )

        # ----------------------------------------------------
        # Other OpenAI output
        # ----------------------------------------------------

        else:

            logger.info(
                "OPENAI OUTPUT | type=%s",
                item_type,
            )


# ============================================================
# OpenAI request
# ============================================================

def create_response(input_data, previous_response_id=None):

    if previous_response_id:

        logger.info(
            "OPENAI REQUEST START | continuation | previous_response_id=%s",
            previous_response_id,
        )

    else:

        logger.info(
            "OPENAI REQUEST START | new conversation"
        )

    logger.info(
        "Sending request to OpenAI..."
    )

    response = client.responses.create(
        model=MODEL,
        tools=tools,
        input=input_data,
        previous_response_id=previous_response_id,
    )

    logger.info(
        "OPENAI RESPONSE RECEIVED | response_id=%s",
        response.id,
    )

    inspect_response(response)

    return response


# ============================================================
# Process MCP approvals
# ============================================================

def process_mcp_approvals(response):

    while True:

        approval_inputs = []

        for item in response.output:

            if item.type == "mcp_approval_request":

                server_label = getattr(
                    item,
                    "server_label",
                    "unknown",
                )

                tool_name = getattr(
                    item,
                    "name",
                    "unknown",
                )

                logger.warning(
                    "MCP APPROVAL REQUIRED"
                )

                logger.warning(
                    "Server: %s",
                    server_label,
                )

                logger.warning(
                    "Tool: %s",
                    tool_name,
                )

                logger.warning(
                    "Approval ID: %s",
                    item.id,
                )

                # ------------------------------------------------
                # Automatically approve
                # ------------------------------------------------

                logger.warning(
                    "MCP APPROVAL -> APPROVING"
                )

                approval_inputs.append(
                    {
                        "type": "mcp_approval_response",
                        "approve": True,
                        "approval_request_id": item.id,
                    }
                )

        # --------------------------------------------------------
        # No approval requests
        # --------------------------------------------------------

        if not approval_inputs:

            logger.info(
                "MCP APPROVAL CHECK -> no pending approvals"
            )

            break

        # --------------------------------------------------------
        # Continue after approval
        # --------------------------------------------------------

        logger.info(
            "MCP APPROVAL -> APPROVED"
        )

        logger.info(
            "MCP EXECUTION -> continuing OpenAI response"
        )

        response = create_response(
            input_data=approval_inputs,
            previous_response_id=response.id,
        )

    return response


# ============================================================
# Main loop
# ============================================================

print()
print("MCP / OpenAI client started.")
print("Logs are being written to logs.txt")
print("Type 'exit' or 'quit' to stop.")
print()

log_stage(
    "APPLICATION READY - WAITING FOR USER INPUT"
)


while True:

    user_input = input("\nAsk a question: ").strip()

    if user_input.lower() in ["exit", "quit"]:

        log_stage(
            "APPLICATION STOPPED"
        )

        break

    if not user_input:
        continue

    try:

        # ----------------------------------------------------
        # User request
        # ----------------------------------------------------

        log_stage(
            "NEW USER REQUEST"
        )

        logger.info(
            "User input: %s",
            user_input,
        )

        # ----------------------------------------------------
        # Initial OpenAI request / MCP discovery
        # ----------------------------------------------------

        log_stage(
            "OPENAI REQUEST / MCP DISCOVERY"
        )

        response = create_response(
            input_data=user_input
        )

        # ----------------------------------------------------
        # MCP approvals
        # ----------------------------------------------------

        response = process_mcp_approvals(
            response
        )

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        log_stage(
            "REQUEST COMPLETE"
        )
        subprocess.run(
        "cls" if os.name == "nt" else "clear",
        shell=True
        )
        print("\n" + "=" * 80)
        print(response.output_text)
        print("=" * 80)

        # ----------------------------------------------------
        # Usage
        # ----------------------------------------------------

        if response.usage:

            usage = response.usage

            print(
                f"\nResponse ID: {response.id}\n"
                f"Model: {response.model}\n"
                f"Input Tokens: {usage.input_tokens}\n"
                f"Output Tokens: {usage.output_tokens}\n"
                f"Total Tokens: {usage.total_tokens}\n"
            )

            logger.info(
                "TOKEN USAGE | input=%s | output=%s | total=%s",
                usage.input_tokens,
                usage.output_tokens,
                usage.total_tokens,
            )

    except Exception as ex:

        logger.exception(
            "REQUEST FAILED"
        )

        print(
            f"\nERROR: {ex}\n"
        )
