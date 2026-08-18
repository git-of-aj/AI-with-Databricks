import os
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


# ============================================================
# Configuration
# ============================================================

load_dotenv()

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
AGENT_NAME = os.getenv("AGENT_NAME")

if not PROJECT_ENDPOINT:
    raise RuntimeError("PROJECT_ENDPOINT is not set")

if not AGENT_NAME:
    raise RuntimeError("AGENT_NAME is not set")


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# Azure clients
# ============================================================

credential = DefaultAzureCredential()

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
)

openai_client = project_client.get_openai_client()


# ============================================================
# Application lifecycle
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FastAPI application")
    logger.info("Azure Foundry endpoint: %s", PROJECT_ENDPOINT)
    logger.info("Azure Foundry agent: %s", AGENT_NAME)

    yield

    logger.info("Shutting down FastAPI application")

    try:
        project_client.close()
    except Exception:
        logger.exception("Error while closing Azure project client")


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title="Azure Foundry Agent API",
    description="FastAPI wrapper around a Microsoft Foundry Agent",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# CORS
# ============================================================

# For development you can allow your frontend.
#
# IMPORTANT:
# In production, replace "*" with your actual frontend URL(s).
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request / Response models
# ============================================================

class CreateConversationResponse(BaseModel):
    conversation_id: str


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Message to send to the Agent",
    )

    conversation_id: str | None = Field(
        default=None,
        description=(
            "Existing Foundry conversation ID. "
            "If omitted, a new conversation is created."
        ),
    )


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


# ============================================================
# Health check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "agent": AGENT_NAME,
    }


# ============================================================
# Create a new conversation
# ============================================================

@app.post(
    "/conversations",
    response_model=CreateConversationResponse,
)
def create_conversation():
    """
    Create a new durable Foundry conversation.

    The returned conversation_id should be stored by the
    frontend/application and sent with subsequent /chat calls.
    """

    try:
        conversation = openai_client.conversations.create()

        logger.info(
            "Created conversation: %s",
            conversation.id,
        )

        return CreateConversationResponse(
            conversation_id=conversation.id
        )

    except Exception as exc:
        logger.exception("Failed to create conversation")

        raise HTTPException(
            status_code=500,
            detail="Failed to create Azure conversation",
        ) from exc


# ============================================================
# Chat with the Agent
# ============================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    """
    Send a message to the Foundry Agent.

    If conversation_id is supplied:
        Continue that conversation.

    If conversation_id is omitted:
        Create a new conversation first.
    """

    try:

        # ----------------------------------------------------
        # Create conversation if necessary
        # ----------------------------------------------------

        conversation_id = request.conversation_id

        if not conversation_id:

            conversation = openai_client.conversations.create()

            conversation_id = conversation.id

            logger.info(
                "Created new conversation: %s",
                conversation_id,
            )

        # ----------------------------------------------------
        # Call the Agent
        # ----------------------------------------------------

        response = openai_client.responses.create(
            conversation=conversation_id,

            input=request.message,

            extra_body={
                "agent_reference": {
                    "name": AGENT_NAME,
                    "type": "agent_reference",
                }
            },
        )

        # ----------------------------------------------------
        # Extract Agent response
        # ----------------------------------------------------

        output_text = response.output_text

        logger.info(
            "Agent response generated. conversation=%s",
            conversation_id,
        )

        return ChatResponse(
            response=output_text,
            conversation_id=conversation_id,
        )

    except Exception as exc:

        logger.exception(
            "Error calling Azure Foundry Agent"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to get response from Azure Agent",
        ) from exc


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Azure Foundry Agent API is running",
        "agent": AGENT_NAME,
        "docs": "/docs",
    }