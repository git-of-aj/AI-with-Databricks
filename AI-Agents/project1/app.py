import os
import sqlite3
import uuid
from typing import Any

from dotenv import load_dotenv
from flask import Flask, request, make_response, render_template_string

from agent_framework import Agent, AgentSession, ContextProvider, SessionContext
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv()

app = Flask(__name__)

DB = "memory.db"


# ---------------------------------------------------------
# Persistent user memory
# ---------------------------------------------------------

def init_db():
    with sqlite3.connect(DB) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                user_name TEXT
            )
        """)
        db.commit()


def get_user(user_id: str) -> dict[str, Any]:
    with sqlite3.connect(DB) as db:
        row = db.execute(
            "SELECT user_name FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    return {"user_name": row[0] if row else None}


def save_user(user_id: str, user_name: str):
    with sqlite3.connect(DB) as db:
        db.execute("""
            INSERT INTO users (user_id, user_name)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET user_name = excluded.user_name
        """, (user_id, user_name))
        db.commit()


# ---------------------------------------------------------
# Agent memory provider
# ---------------------------------------------------------

class UserMemoryProvider(ContextProvider):
    """Loads persistent user memory into the agent."""

    DEFAULT_SOURCE_ID = "user_memory"

    def __init__(self):
        super().__init__(self.DEFAULT_SOURCE_ID)

    async def before_run(
        self,
        *,
        agent: Any,
        session: AgentSession | None,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        user_name = state.get("user_name")

        if user_name:
            context.extend_instructions(
                self.source_id,
                f"The user's name is {user_name}. "
                "Always address them by name."
            )
        else:
            context.extend_instructions(
                self.source_id,
                "You don't know the user's name yet. "
                "Ask for it politely when appropriate."
            )

    async def after_run(
        self,
        *,
        agent: Any,
        session: AgentSession | None,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        for msg in context.input_messages:
            text = getattr(msg, "text", "")

            if not isinstance(text, str):
                continue

            lower = text.lower()

            if "my name is" in lower:
                name = (
                    lower
                    .split("my name is", 1)[1]
                    .strip()
                    .split()[0]
                    .capitalize()
                )

                state["user_name"] = name


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------

client = FoundryChatClient(
    project_endpoint=os.environ["ENDPOINT"],
    model=os.environ["MODEL"],
    credential=AzureCliCredential(),
)

agent = Agent(
    client=client,
    name="MemoryAgent",
    instructions="""
You are a friendly assistant.

Keep responses concise.

If you know the user's name, use it naturally in your response.
""",
    context_providers=[UserMemoryProvider()],
)


# ---------------------------------------------------------
# Minimal UI
# ---------------------------------------------------------

HTML = """
<!doctype html>
<html>
<head>
    <title>Agent Memory Demo</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 0 20px;
            color: #222;
        }

        h1 {
            margin-bottom: 5px;
        }

        .memory {
            background: #f1f5f9;
            padding: 12px 16px;
            border-radius: 8px;
            margin: 20px 0;
        }

        input {
            width: 75%;
            padding: 12px;
            font-size: 16px;
        }

        button {
            padding: 12px 18px;
            font-size: 16px;
            cursor: pointer;
        }

        .answer {
            margin-top: 25px;
            padding: 16px;
            background: #eef6ff;
            border-radius: 8px;
            white-space: pre-wrap;
        }

        .reset {
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <h1>🧠 Agent Memory Demo</h1>
    <p>Each browser gets its own persistent user memory.</p>

    <div class="memory">
        <strong>Remembered name:</strong>
        {{ name or "Nothing yet" }}
    </div>

    <form method="post">
        <input
            name="message"
            placeholder="Try: My name is Alice"
            autofocus
            required
        >
        <button type="submit">Send</button>
    </form>

    {% if answer %}
        <div class="answer">
            {{ answer }}
        </div>
    {% endif %}

    <div class="reset">
        <a href="/reset">Reset this user's memory</a>
    </div>
</body>
</html>
"""


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
async def index():
    user_id = request.cookies.get("user_id")

    if not user_id:
        user_id = str(uuid.uuid4())

    user = get_user(user_id)

    answer = None

    if request.method == "POST":
        message = request.form["message"]

        # Create a fresh AgentSession for this invocation.
        session = agent.create_session(session_id=user_id)

        # Load durable memory into the provider's session state.
        session.state["user_memory"] = {
            "user_name": user["user_name"]
        }

        result = await agent.run(
            message,
            session=session,
        )

        # Provider may have learned something during the run.
        memory = session.state.get("user_memory", {})
        user_name = memory.get("user_name")

        if user_name:
            save_user(user_id, user_name)

        answer = result.text
        user["user_name"] = user_name

    response = make_response(
        render_template_string(
            HTML,
            name=user["user_name"],
            answer=answer,
        )
    )

    response.set_cookie(
        "user_id",
        user_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax",
    )

    return response


@app.route("/reset")
def reset():
    user_id = request.cookies.get("user_id")

    if user_id:
        with sqlite3.connect(DB) as db:
            db.execute(
                "DELETE FROM users WHERE user_id = ?",
                (user_id,),
            )
            db.commit()

    response = make_response(
        '<p>Memory reset.</p><p><a href="/">Back</a></p>'
    )

    response.set_cookie("user_id", "", expires=0)

    return response


# ---------------------------------------------------------

init_db()

if __name__ == "__main__":
    app.run(debug=True)
