import os
import re
import json

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# Environment variables
# ============================================================

ENDPOINT = os.getenv("OPENAI_ENDPOINT")
MODEL = os.getenv("OPENAI_DEPLOYMENT")
API_KEY = os.getenv("OPENAI_API_KEY")

GITHUB_MCP_PAT = os.getenv("GITHUB_MCP_PAT")

# ------------------------------------------------------------
# SLM / Phi-4 configuration
# ------------------------------------------------------------

PHI4_ENDPOINT = os.getenv("PHI4_ENDPOINT")
PHI4_MODEL = os.getenv("PHI4_MODEL")
PHI4_API_KEY = os.getenv("PHI4_API_KEY")


# ============================================================
# Routes
# ============================================================

ROUTES = {

    "github": [
        "github",
        "git hub",
        "repository",
        "repo",
        "pull request",
        "pull requests",
        "github actions",
        "github workflow",
        "branch",
        "commit",
        "issue",
    ],

    "microsoft_learn": [
        "microsoft",
        "azure",
        ".net",
        "dotnet",
        "power apps",
        "power automate",
        "microsoft 365",
        "office 365",
        "windows server",
        "powershell",
        "visual studio",
        "asp.net",
    ],

    "web": [
        "search the web",
        "search online",
        "latest news",
        "current news",
        "what happened today",
        "look it up",
        "search internet",
    ],
}


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
        "Use this tool for any request related to GitHub. "
        "If the user requests branch or Pull Request creation, "
        "repo details, issues, commits, files, or other GitHub operations, "
        "use the appropriate GitHub tool. "
        "Always use GitHub Account git-of-aj."
    ),
    "headers": {
        "Authorization": f"Bearer {GITHUB_MCP_PAT}"
    },
}


web_search = {
    "type": "web_search"
}


# ============================================================
# Route -> actual OpenAI tool
# ============================================================

MCP_ROUTES = {
    "github": github_mcp,
    "microsoft_learn": microsoft_learn_mcp,
    "web": web_search,
}


# ============================================================
# Simple router
# ============================================================

def keyword_matches(query: str, keyword: str) -> bool:
    """
    Match phrases safely.

    Examples:

        "github branch" -> matches "github"
        "create a commit" -> matches "commit"

    But:

        "I am committed" -> does not match "commit"
    """

    query = query.lower().strip()
    keyword = keyword.lower().strip()

    # Multi-word phrases
    if " " in keyword:
        return keyword in query

    # Single words
    return re.search(
        rf"\b{re.escape(keyword)}\b",
        query,
        re.IGNORECASE,
    ) is not None


def simple_router(query: str):
    """
    Fast deterministic router.

    Returns:

        ["github"]
        ["microsoft_learn"]
        ["web"]

    or:

        None

    None means the query is ambiguous and should
    be sent to the SLM router.
    """

    query_lower = query.lower().strip()

    # --------------------------------------------------------
    # Obviously no-tool queries
    # --------------------------------------------------------

    no_tool_queries = {
        "hi",
        "hello",
        "hey",
        "hi there",
        "hello there",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "thanks!",
        "thank you!",
        "how are you",
        "how are you?",
    }

    if query_lower in no_tool_queries:
        return ["none"]

    # --------------------------------------------------------
    # Keyword routing
    # --------------------------------------------------------

    matched_routes = []

    for route, keywords in ROUTES.items():

        for keyword in keywords:

            if keyword_matches(query, keyword):

                matched_routes.append(route)

                break

    # --------------------------------------------------------
    # No match -> ambiguous
    # --------------------------------------------------------

    if not matched_routes:
        return None

    return matched_routes


# ============================================================
# SLM router
# ============================================================

def slm_router(
    query: str,
    router_client: OpenAI,
):
    """
    Use Phi-4 / SLM for ambiguous queries.

    The SLM does NOT receive MCP tools.

    It only decides which route should be used.
    """

    prompt = f"""
You are a routing classifier.

Your only job is to decide which external tool/server is
needed for the user's request.

Available routes:

github:
- GitHub repositories
- GitHub branches
- commits
- pull requests
- issues
- GitHub Actions
- GitHub files and code

microsoft_learn:
- Microsoft documentation
- Azure
- .NET
- Power Apps
- Power Automate
- Microsoft 365
- Windows Server
- PowerShell
- Visual Studio
- Microsoft technologies

web:
- current information
- news
- internet searches
- information that requires web browsing

none:
- casual conversation
- greetings
- simple questions that do not require external tools
- general knowledge that does not require the above tools

A query may require multiple routes.

User query:
{query}

Return ONLY valid JSON.

Format:

{{
    "routes": ["github"],
    "confidence": 0.95
}}

Valid route names:

github
microsoft_learn
web
none

Do not return explanations.
"""

    try:

        response = router_client.responses.create(
            model=PHI4_MODEL,
            input=prompt,
        )

        text = response.output_text.strip()

        result = json.loads(text)

        routes = result.get("routes", [])
        confidence = float(
            result.get("confidence", 0)
        )

        valid_routes = {
            "github",
            "microsoft_learn",
            "web",
            "none",
        }

        # ----------------------------------------------------
        # Validate routes
        # ----------------------------------------------------

        routes = [
            route
            for route in routes
            if route in valid_routes
        ]

        # ----------------------------------------------------
        # If SLM returned none together with another route,
        # remove none.
        # ----------------------------------------------------

        if len(routes) > 1 and "none" in routes:

            routes.remove("none")

        # ----------------------------------------------------
        # Empty result -> none
        # ----------------------------------------------------

        if not routes:

            routes = ["none"]

        return {
            "routes": routes,
            "confidence": confidence,
            "source": "slm",
        }

    except Exception as ex:

        print(
            f"\nWARNING: SLM router failed: {ex}"
        )

        print(
            "WARNING: Falling back to no MCP tools."
        )

        return {
            "routes": ["none"],
            "confidence": 0.0,
            "source": "slm_error",
        }


# ============================================================
# Hybrid router
# ============================================================

def hybrid_router(
    query: str,
    router_client: OpenAI,
):
    """
    Hybrid routing:

    1. Simple keyword router
    2. If ambiguous -> Phi-4
    """

    # --------------------------------------------------------
    # Fast router
    # --------------------------------------------------------

    simple_routes = simple_router(query)

    if simple_routes is not None:

        return {
            "routes": simple_routes,
            "confidence": 1.0,
            "source": "simple",
        }

    # --------------------------------------------------------
    # Ambiguous -> SLM
    # --------------------------------------------------------

    print(
        "\nINFO: Simple router could not determine route."
    )

    print(
        "INFO: Sending query to SLM router..."
    )

    return slm_router(
        query=query,
        router_client=router_client,
    )


# ============================================================
# Get tools selected by router
# ============================================================

def get_selected_tools(route_result):
    """
    Convert router routes into actual OpenAI tools.

    IMPORTANT:

    If route is "none", this returns [].

    Therefore the main GPT model receives NO MCP tools.
    """

    routes = route_result.get("routes", [])

    # --------------------------------------------------------
    # No external tool required
    # --------------------------------------------------------

    if not routes or "none" in routes:

        return []

    selected_tools = []

    for route in routes:

        tool = MCP_ROUTES.get(route)

        if tool is None:
            continue

        selected_tools.append(tool)

    return selected_tools


# ============================================================
# Display routing result
# ============================================================

def display_routing_result(
    route_result,
    selected_tools,
):
    """
    Display exactly what the router decided.
    """

    routes = route_result.get("routes", [])
    source = route_result.get("source", "unknown")
    confidence = route_result.get("confidence", 0)

    print("\n" + "-" * 80)
    print("ROUTER RESULT")
    print("-" * 80)

    print(f"Router source : {source}")
    print(f"Routes        : {routes}")
    print(f"Confidence    : {confidence:.2f}")

    # --------------------------------------------------------
    # No tools
    # --------------------------------------------------------

    if not selected_tools:

        print(
            "\nWARNING: Router detected NO MCP tools."
        )

        print(
            "WARNING: Sending request with tools=[]"
        )

    # --------------------------------------------------------
    # Tools detected
    # --------------------------------------------------------

    else:

        print(
            "\nWARNING: Router detected MCP tool(s):"
        )

        for tool in selected_tools:

            tool_type = tool.get(
                "type",
                "unknown",
            )

            server_label = tool.get(
                "server_label",
                tool_type,
            )

            print(
                f"WARNING: Router detected MCP tool: "
                f"{server_label}"
            )

    print("-" * 80)


# ============================================================
# Main AI function
# ============================================================

def ai():

    # ========================================================
    # Main GPT client
    # ========================================================

    client = OpenAI(
        base_url=ENDPOINT,
        api_key=API_KEY,
    )

    # ========================================================
    # SLM client
    # ========================================================

    router_client = OpenAI(
        base_url=PHI4_ENDPOINT,
        api_key=PHI4_API_KEY,
    )

    # ========================================================
    # Process MCP approvals
    # ========================================================

    def process_mcp_approvals(
        response,
        selected_tools,
    ):
        """
        Continue an MCP request after approval.

        IMPORTANT:

        selected_tools is the exact tool list selected
        by the router for this request.

        We DO NOT use the global list of all MCP tools.
        """

        while True:

            approval_inputs = []

            for item in response.output:

                if item.type == "mcp_approval_request":

                    print(
                        "\nMCP approval requested:"
                    )

                    print(
                        f"  Server: "
                        f"{getattr(item, 'server_label', 'unknown')}"
                    )

                    print(
                        f"  Tool:   "
                        f"{getattr(item, 'name', 'unknown')}"
                    )

                    print(
                        f"  ID:     "
                        f"{item.id}"
                    )

                    approval_inputs.append(
                        {
                            "type": "mcp_approval_response",
                            "approve": True,
                            "approval_request_id": item.id,
                        }
                    )

            # ------------------------------------------------
            # No more approval requests
            # ------------------------------------------------

            if not approval_inputs:

                break

            print(
                "\nAutomatically approving MCP request(s)..."
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # Reuse ONLY the selected tools.
            # ------------------------------------------------

            response = client.responses.create(
                model=MODEL,
                tools=selected_tools,
                input=approval_inputs,
                previous_response_id=response.id,
            )

        return response

    # ========================================================
    # User loop
    # ========================================================

    print()
    print("=" * 80)
    print("Hybrid MCP Router")
    print("=" * 80)

    print(
        "Type 'exit' or 'quit' to stop."
    )

    print()

    while True:

        user_input = input(
            "Ask a question: "
        ).strip()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if user_input.lower() in [
            "exit",
            "quit",
        ]:

            break

        if not user_input:
            continue

        try:

            # =================================================
            # ROUTING
            # =================================================

            print(
                "\nRouting request..."
            )

            route_result = hybrid_router(
                query=user_input,
                router_client=router_client,
            )

            # =================================================
            # SELECT TOOLS
            # =================================================

            selected_tools = get_selected_tools(
                route_result
            )

            # =================================================
            # DISPLAY ROUTING
            # =================================================

            display_routing_result(
                route_result,
                selected_tools,
            )

            # =================================================
            # MAIN GPT REQUEST
            # =================================================

            print(
                "\nSending request to main model..."
            )

            print(
                f"Tools supplied to GPT: "
                f"{len(selected_tools)}"
            )

            response = client.responses.create(
                model=MODEL,

                # ------------------------------------------------
                # THIS IS THE IMPORTANT PART
                #
                # If no MCP was detected:
                #
                #     tools=[]
                #
                # If GitHub was detected:
                #
                #     tools=[github_mcp]
                #
                # etc.
                # ------------------------------------------------

                tools=selected_tools,

                input=user_input,
            )

            # =================================================
            # MCP APPROVALS
            # =================================================

            response = process_mcp_approvals(
                response=response,
                selected_tools=selected_tools,
            )

            # =================================================
            # FINAL RESPONSE
            # =================================================

            print(
                "\n" + "=" * 80
            )

            print(
                response.output_text
            )

            print(
                "=" * 80
            )

            # =================================================
            # TOKEN USAGE
            # =================================================

            if response.usage:

                usage = response.usage

                print(
                    f"\nID: {response.id}\n"
                    f"Model: {response.model}\n"
                    f"Input Tokens: "
                    f"{usage.input_tokens}\n"
                    f"Output Tokens: "
                    f"{usage.output_tokens}\n"
                    f"Total Tokens: "
                    f"{usage.total_tokens}\n"
                )

        except Exception as ex:

            print(
                f"\nERROR: {ex}\n"
            )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":

    ai()
