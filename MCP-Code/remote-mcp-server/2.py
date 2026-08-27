import asyncio
import json
import logging
from datetime import datetime, timezone

from azure.identity.aio import AzureCliCredential
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient


LOG_FILE = "logs.txt"


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logger = logging.getLogger("mcp_debug")
logger.setLevel(logging.DEBUG)

# Avoid duplicate handlers if this file is imported/reloaded
if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a",
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log(message: str):
    """Log to both console and logs.txt."""
    logger.info(message)
    print(message)


def log_separator(title: str = ""):
    line = "=" * 80

    if title:
        log(f"\n{line}\n{title}\n{line}")
    else:
        log(line)


def serialize(value):
    """Safely convert values to something JSON/log friendly."""
    try:
        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    except Exception:
        return str(value)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():

    log_separator("APPLICATION START")

    log(f"Python MCP Host starting")
    log(f"Log file: {LOG_FILE}")

    # -----------------------------------------------------------------------
    # Azure authentication
    # -----------------------------------------------------------------------

    log_separator("AZURE AUTHENTICATION")

    log("Creating AzureCliCredential...")

    async with AzureCliCredential() as credential:

        log("AzureCliCredential created.")

        # -------------------------------------------------------------------
        # Foundry client
        # -------------------------------------------------------------------

        log_separator("FOUNDRY CLIENT INITIALIZATION")

        log("Creating FoundryChatClient...")

        client = FoundryChatClient(
            project_endpoint=(
                "https://foundry0309.services.ai.azure.com/"
                "api/projects/proj-default"
            ),
            model="gpt-5-mini",
            credential=credential,
        )

        log("FoundryChatClient created.")
        log("Model: gpt-5-mini")

        # -------------------------------------------------------------------
        # MCP tool configuration
        # -------------------------------------------------------------------

        log_separator("MCP TOOL CONFIGURATION")

        mcp_url = "https://learn.microsoft.com/api/mcp"

        log("Creating Microsoft Learn hosted MCP tool...")
        log(f"MCP URL: {mcp_url}")
        log("Approval mode: never_require")

        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn",
            url=mcp_url,
            approval_mode="never_require",
        )

        log("Microsoft Learn MCP tool configuration created.")
        log(
            "IMPORTANT: get_mcp_tool() creates a Foundry-hosted MCP "
            "tool configuration."
        )
        log(
            "The actual MCP connection/tool execution occurs in the "
            "Foundry service, not in this Python process."
        )

        # -------------------------------------------------------------------
        # Agent creation
        # -------------------------------------------------------------------

        log_separator("AGENT INITIALIZATION")

        log("Creating Agent...")

        async with Agent(
            client=client,
            name="AzureDocumentationAgent",
            instructions="""
            You are an expert Microsoft Azure documentation assistant.

            IMPORTANT:
            - Use the Microsoft Learn MCP tool whenever it is relevant.
            - Do not answer Azure documentation questions from your
              general knowledge when Microsoft Learn can provide the answer.
            - Prefer information retrieved from Microsoft Learn.
            """,
            tools=[learn_mcp],
        ) as agent:

            log("Agent created successfully.")
            log("Microsoft Learn MCP tool supplied to agent.")

            # ---------------------------------------------------------------
            # User query
            # ---------------------------------------------------------------

            query = (
                "How do I configure managed identity for an Azure Function?"
            )

            log_separator("USER QUERY")

            log(f"User: {query}")

            # ---------------------------------------------------------------
            # Run agent using STREAMING
            # ---------------------------------------------------------------

            log_separator("AGENT RUN START")

            log("Starting agent.run(..., stream=True)")
            log("Waiting for GPT-5 response/events...")

            response_stream = agent.run(
                query,
                stream=True,
            )

            final_response = None

            try:

                async for update in response_stream:

                    # -------------------------------------------------------
                    # Inspect every content item returned by Agent Framework
                    # -------------------------------------------------------

                    for content in update.contents:

                        content_type = getattr(
                            content,
                            "type",
                            None,
                        )

                        # ===================================================
                        # TEXT
                        # ===================================================

                        if content_type == "text":

                            text = getattr(
                                content,
                                "text",
                                "",
                            )

                            if text:
                                log(f"[LLM TEXT] {text}")

                        # ===================================================
                        # MCP / FUNCTION CALL
                        # ===================================================

                        elif content_type == "function_call":

                            tool_name = getattr(
                                content,
                                "name",
                                None,
                            )

                            call_id = getattr(
                                content,
                                "call_id",
                                None,
                            )

                            arguments = getattr(
                                content,
                                "arguments",
                                None,
                            )

                            log_separator("MCP / TOOL CALL DETECTED")

                            log(f"Tool name: {tool_name}")
                            log(f"Call ID: {call_id}")
                            log(
                                "Arguments:\n"
                                + serialize(arguments)
                            )

                            # This is the important evidence:
                            log(
                                ">>> GPT requested a tool call."
                            )

                            if tool_name:
                                log(
                                    f">>> Tool selected: {tool_name}"
                                )

                        # ===================================================
                        # TOOL RESULT
                        # ===================================================

                        elif content_type == "function_result":

                            call_id = getattr(
                                content,
                                "call_id",
                                None,
                            )

                            result = getattr(
                                content,
                                "result",
                                None,
                            )

                            log_separator("MCP / TOOL RESULT")

                            log(f"Call ID: {call_id}")

                            log(
                                "Result:\n"
                                + serialize(result)
                            )

                            log(
                                ">>> Tool execution returned a result."
                            )

                        # ===================================================
                        # APPROVAL REQUEST
                        # ===================================================

                        elif content_type == "function_approval_request":

                            log_separator(
                                "MCP TOOL APPROVAL REQUEST"
                            )

                            log(
                                ">>> Agent Framework received a "
                                "tool approval request."
                            )

                            log(
                                serialize(content)
                            )

                        # ===================================================
                        # APPROVAL RESPONSE
                        # ===================================================

                        elif content_type == "function_approval_response":

                            log_separator(
                                "MCP TOOL APPROVAL RESPONSE"
                            )

                            log(
                                serialize(content)
                            )

                        # ===================================================
                        # USAGE
                        # ===================================================

                        elif content_type == "usage":

                            log_separator("MODEL USAGE")

                            log(
                                serialize(content)
                            )

                        # ===================================================
                        # ERROR
                        # ===================================================

                        elif content_type == "error":

                            log_separator("AGENT ERROR")

                            log(
                                serialize(content)
                            )

                        # ===================================================
                        # UNKNOWN CONTENT
                        # ===================================================

                        else:

                            log(
                                f"[OTHER CONTENT] "
                                f"type={content_type}"
                            )

                            log(
                                serialize(content)
                            )

                # -----------------------------------------------------------
                # Get final aggregated response
                # -----------------------------------------------------------

                final_response = (
                    await response_stream.get_final_response()
                )

            except Exception as exc:

                log_separator("AGENT RUN EXCEPTION")

                log(
                    f"Exception type: {type(exc).__name__}"
                )

                log(
                    f"Exception: {exc}"
                )

                raise

            # ---------------------------------------------------------------
            # Final answer
            # ---------------------------------------------------------------

            log_separator("FINAL LLM ANSWER")

            if final_response is not None:

                log(
                    final_response.text
                )

                log_separator("FINAL RESPONSE OBJECT")

                log(
                    f"Response ID: "
                    f"{getattr(final_response, 'response_id', None)}"
                )

                log(
                    f"Messages: "
                    f"{len(getattr(final_response, 'messages', []))}"
                )

            else:

                log("No final response received.")

            log_separator("AGENT RUN COMPLETE")

    log_separator("APPLICATION COMPLETE")


if __name__ == "__main__":
    asyncio.run(main())
