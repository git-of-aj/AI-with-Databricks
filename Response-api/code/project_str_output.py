from fastapi import FastAPI
from pydantic import BaseModel
from template import get_openai_client
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = get_openai_client()
ai_model_name = "gpt-5-mini"

# ============================================================
# Request models
# ============================================================

class TicketRequest(BaseModel):
    message: str


# ============================================================
# OpenAI structured output
# ============================================================

class SupportTicket(BaseModel):
    category: str
    issue: str
    priority: str
    sentiment: str
    recommended_team: str
    needs_human: bool


# ============================================================
# Ticket creation payload
# ============================================================

class CreateTicketRequest(BaseModel):
    category: str
    issue: str
    priority: str
    sentiment: str
    recommended_team: str
    needs_human: bool


# ============================================================
# Ticket creation response
# ============================================================

class CreateTicketResponse(BaseModel):
    ticket_number: int
    category: str
    issue: str
    priority: str
    sentiment: str
    recommended_team: str
    needs_human: bool


# ============================================================
# CREATE TICKET ENDPOINT
# ============================================================

@app.post("/create-ticket", response_model=CreateTicketResponse)
def create_ticket(ticket: CreateTicketRequest):

    # Mimic ticket creation
    ticket_number = random.randint(10000, 99999)

    return CreateTicketResponse(
        ticket_number=ticket_number,
        category=ticket.category,
        issue=ticket.issue,
        priority=ticket.priority,
        sentiment=ticket.sentiment,
        recommended_team=ticket.recommended_team,
        needs_human=ticket.needs_human,
    )


# ============================================================
# CLASSIFY ENDPOINT
# ============================================================

@app.post("/classify")
def classify_ticket(request: TicketRequest):

    # --------------------------------------------------------
    # Ask OpenAI to classify the user's request
    # --------------------------------------------------------

    response = client.responses.parse(
        model=ai_model_name,
        input=[
            {
                "role": "system",
                "content": """
You are a customer support ticket classifier.

Analyze the customer's message and classify it.

Scope:
You must classify requests that ask for assistance or guidance
in the following categories. Basic greetings are allowed.

You must respectfully deny any out-of-scope question.

category must be one of:
- billing
- technical
- HR
- account
- other
- out of scope

Definitions:
- billing: Billing, payment, invoice, or subscription issues
- technical: Technical problems, errors, bugs, or troubleshooting
- HR: Human resources-related questions
- account: Account, login, password, or profile-related issues
- other: Basic greetings or general conversation that does not require a support ticket
- out of scope: Questions unrelated to the supported categories

Important:
- Basic greetings such as "Hi", "Hello", or "How are you?"
  must be categorized as "other".
- "other" must NEVER result in a support ticket.
- "out of scope" must NEVER result in a support ticket.
- Only billing, technical, HR, and account categories should
  result in a support ticket.

priority must be one of:
- low
- medium
- high

sentiment must be one of:
- positive: If the user tone is happy
- neutral: If the user does not use any strong or bad language
- frustrated: If the user seems very unhappy, impatient, or angry

Decide whether a human should review the ticket.

For any out-of-scope question, mark every field as N/A.
""",
            },
            {
                "role": "user",
                "content": request.message,
            },
        ],
        text_format=SupportTicket,
    )

    # --------------------------------------------------------
    # Get structured JSON returned by OpenAI
    # --------------------------------------------------------

    ticket = response.output_parsed

    # --------------------------------------------------------
    # Only these categories should create a ticket
    # --------------------------------------------------------

    ticket_categories = {
        "billing",
        "technical",
        "HR",
        "account",
    }

    # --------------------------------------------------------
    # OUT OF SCOPE
    # Do NOT create a ticket
    # --------------------------------------------------------

    if ticket.category == "out of scope":
        return {
            "message": (
                "Please ask in-scope questions like: "
                "How do I reset my password?"
            )
        }

    # --------------------------------------------------------
    # OTHER / GENERAL CONVERSATION
    # Do NOT create a ticket
    # --------------------------------------------------------

    if ticket.category not in ticket_categories:
        return {
            "message": (
                "Hello! How can I help you with billing, technical, "
                "HR, or account-related questions?"
            )
        }

    # --------------------------------------------------------
    # IN-SCOPE SUPPORT REQUEST
    # Create a ticket
    # --------------------------------------------------------

    create_ticket_payload = CreateTicketRequest(
        category=ticket.category,
        issue=ticket.issue,
        priority=ticket.priority,
        sentiment=ticket.sentiment,
        recommended_team=ticket.recommended_team,
        needs_human=ticket.needs_human,
    )

    # Call the ticket creation function directly.
    created_ticket = create_ticket(create_ticket_payload)

    # --------------------------------------------------------
    # Return simple message for the webapp/user
    # --------------------------------------------------------

    return {
        "message": (
            f"{created_ticket.ticket_number} created and forwarded "
            f"to {created_ticket.recommended_team}"
        ),
        "ticket": created_ticket,
    }
