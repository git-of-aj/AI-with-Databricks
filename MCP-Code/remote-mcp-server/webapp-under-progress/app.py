import json
import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import jwt

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from azure.identity.aio import OnBehalfOfCredential
from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient


load_dotenv()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TENANT_ID = os.environ["TENANT_ID"]
API_CLIENT_ID = os.environ["API_CLIENT_ID"]
API_CLIENT_SECRET = os.environ["API_CLIENT_SECRET"]

FOUNDRY_PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
FOUNDRY_MODEL = os.getenv("FOUNDRY_MODEL", "gpt-5-mini")

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:8000",
)

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# v2.0 issuer
ISSUER = f"{AUTHORITY}/v2.0"

# Microsoft Entra v2 JWKS endpoint
JWKS_URL = f"{AUTHORITY}/discovery/v2.0/keys"


# ---------------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Foundry OBO Agent API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

_jwks_client = jwt.PyJWKClient(JWKS_URL)


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """
    Validate the access token issued by Microsoft Entra ID.

    The browser must send:

        Authorization: Bearer <token>

    The token must have this API's client ID as its audience.
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must use Bearer",
        )

    token = authorization[7:].strip()

    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=API_CLIENT_ID,
            issuer=ISSUER,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid access token: {exc}",
        ) from exc

    return claims


# ---------------------------------------------------------------------------
# Request/response models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ApprovalRequest(BaseModel):
    approval_id: str
    approved: bool


# ---------------------------------------------------------------------------
# Agent state
# ---------------------------------------------------------------------------

@dataclass
class PendingApproval:
    request: Any
    conversation_id: str
    user_id: str


@dataclass
class Conversation:
    session: Any
    agent: Any
    credential: Any
    client: Any


# ---------------------------------------------------------------------------
# Demo state store
#
# IMPORTANT:
# This is intentionally in-memory.
#
# Production:
#     - store conversation metadata in Redis/DB
#     - store durable agent/thread/session state appropriately
#     - never rely on process memory when running multiple workers
# ---------------------------------------------------------------------------

conversations: dict[str, Conversation] = {}

pending_approvals: dict[str, PendingApproval] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def user_id_from_claims(claims: dict[str, Any]) -> str:
    """
    Prefer oid as the stable Entra object identifier.
    """

    oid = claims.get("oid")

    if not oid:
        raise HTTPException(
            status_code=401,
            detail="Token does not contain oid",
        )

    return oid


def serialize_approval(
    approval_id: str,
    approval_request: Any,
) -> dict[str, Any]:
    """
    Convert Agent Framework's approval request into JSON for the browser.
    """

    function_call = getattr(
        approval_request,
        "function_call",
        None,
    )

    if function_call is None:
        return {
            "approval_id": approval_id,
            "type": "approval",
            "message": "The agent is requesting approval.",
        }

    arguments = getattr(
        function_call,
        "arguments",
        None,
    )

    # Arguments can already be JSON or a string depending on version.
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except Exception:
            pass

    return {
        "approval_id": approval_id,
        "type": "function_approval",
        "tool": getattr(
            function_call,
            "name",
            "unknown",
        ),
        "arguments": arguments,
    }


async def create_conversation(
    user_token: str,
    conversation_id: str,
) -> Conversation:

    """
    Create a Foundry Chat Client using the user's token through OBO.

    The incoming token is the user assertion.

    OnBehalfOfCredential exchanges it for a downstream token that
    represents the user when FastAPI calls Foundry.
    """

    credential = OnBehalfOfCredential(
        tenant_id=TENANT_ID,
        client_id=API_CLIENT_ID,
        client_secret=API_CLIENT_SECRET,
        user_assertion=user_token,
    )

    client = FoundryChatClient(
        project_endpoint=FOUNDRY_PROJECT_ENDPOINT,
        model=FOUNDRY_MODEL,
        credential=credential,
    )

    # -----------------------------------------------------------------------
    # MCP
    #
    # Unlike your original example, we require approval.
    # This means the model cannot invoke the MCP tool until the user
    # explicitly approves it.
    # -----------------------------------------------------------------------

    learn_mcp = client.get_mcp_tool(
        name="Microsoft Learn",
        url="https://learn.microsoft.com/api/mcp",

        # Human-in-the-loop:
        approval_mode="always_require",
    )

    agent = Agent(
        client=client,
        name="AzureDocumentationAgent",
        instructions="""
You are an expert Microsoft Azure documentation assistant.

Use the Microsoft Learn MCP tools whenever they are relevant
to answering the user's question.

Prefer information retrieved from Microsoft Learn.

IMPORTANT:
- MCP tool calls require user approval.
- Do not attempt to bypass an approval request.
- Explain briefly why an MCP tool call is useful when appropriate.
""",
        tools=[learn_mcp],
    )

    session = agent.create_session()

    conversation = Conversation(
        session=session,
        agent=agent,
        credential=credential,
        client=client,
    )

    conversations[conversation_id] = conversation

    return conversation


async def get_or_create_conversation(
    user_token: str,
    user_id: str,
    conversation_id: str | None,
) -> tuple[str, Conversation]:

    if not conversation_id:
        conversation_id = secrets.token_urlsafe(24)

    conversation = conversations.get(conversation_id)

    if conversation:
        return conversation_id, conversation

    conversation = await create_conversation(
        user_token=user_token,
        conversation_id=conversation_id,
    )

    return conversation_id, conversation


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
):
    """
    Execute an agent request.

    Possible responses:

        {
          "status": "completed",
          "conversation_id": "...",
          "text": "..."
        }

    or:

        {
          "status": "approval_required",
          "conversation_id": "...",
          "approval": {...}
        }
    """

    authorization = http_request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    user_token = authorization[7:].strip()

    user_id = user_id_from_claims(current_user)

    conversation_id, conversation = (
        await get_or_create_conversation(
            user_token=user_token,
            user_id=user_id,
            conversation_id=request.conversation_id,
        )
    )

    # Run the agent.
    result = await conversation.agent.run(
        request.message,
        session=conversation.session,
    )

    # ---------------------------------------------------------------
    # Human-in-the-loop approval
    # ---------------------------------------------------------------

    if result.user_input_requests:

        approvals = []

        for approval_request in result.user_input_requests:

            approval_id = secrets.token_urlsafe(24)

            pending_approvals[approval_id] = PendingApproval(
                request=approval_request,
                conversation_id=conversation_id,
                user_id=user_id,
            )

            approvals.append(
                serialize_approval(
                    approval_id,
                    approval_request,
                )
            )

        return {
            "status": "approval_required",
            "conversation_id": conversation_id,
            "approvals": approvals,
        }

    return {
        "status": "completed",
        "conversation_id": conversation_id,
        "text": result.text,
    }


# ---------------------------------------------------------------------------
# Approval
# ---------------------------------------------------------------------------

@app.post("/api/approval")
async def approval(
    request: ApprovalRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
):
    """
    Continue a paused agent run after user approval/rejection.
    """

    authorization = http_request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    user_id = user_id_from_claims(current_user)

    pending = pending_approvals.get(request.approval_id)

    if not pending:
        raise HTTPException(
            status_code=404,
            detail="Approval request no longer exists",
        )

    # Do not allow another user to approve someone else's request.
    if pending.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Approval belongs to another user",
        )

    conversation = conversations.get(
        pending.conversation_id
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation no longer exists",
        )

    approval_request = pending.request

    # Create Agent Framework approval response.
    approval_message = Message(
        role="user",
        contents=[
            approval_request.to_function_approval_response(
                request.approved
            )
        ],
    )

    # Remove the pending request before continuing.
    pending_approvals.pop(
        request.approval_id,
        None,
    )

    # Continue the same agent session.
    result = await conversation.agent.run(
        approval_message,
        session=conversation.session,
    )

    # It is possible that another tool requires approval.
    if result.user_input_requests:

        approvals = []

        for next_request in result.user_input_requests:

            approval_id = secrets.token_urlsafe(24)

            pending_approvals[approval_id] = PendingApproval(
                request=next_request,
                conversation_id=pending.conversation_id,
                user_id=user_id,
            )

            approvals.append(
                serialize_approval(
                    approval_id,
                    next_request,
                )
            )

        return {
            "status": "approval_required",
            "conversation_id": pending.conversation_id,
            "approvals": approvals,
        }

    return {
        "status": "completed",
        "conversation_id": pending.conversation_id,
        "text": result.text,
    }


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "foundry-fastapi-agent",
    }
