import asyncio
import os
import re
from dotenv import load_dotenv

load_dotenv("../.env")

from agent_framework import (
    Agent,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    handler,
)
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from typing_extensions import Never


# ---------------------------------------------------------
# Create the Foundry client and agent once
# ---------------------------------------------------------

credential = AzureCliCredential()

foundry_client = FoundryChatClient(
    project_endpoint=os.environ["ENDPOINT"],
    model=os.environ["MODEL"],
    credential=credential,
)

summarizer_agent = Agent(
    client=foundry_client,
    name="MeetingSummarizer",
    instructions="""
You are a meeting summarization assistant.

Given a meeting transcript, produce a concise daily standup summary.

Include:
- Key updates
- Decisions made
- Blockers
- Action items

Do not invent information that is not present in the transcript.
Keep the output concise and professional.
""",
)


# ---------------------------------------------------------
# Helper: Read TXT or VTT transcript
# ---------------------------------------------------------

def read_transcript_file(filename: str) -> str:
    """
    Read a .txt or .vtt meeting transcript.

    For .txt:
        Return the file contents as-is.

    For .vtt:
        Remove WebVTT headers, timestamps, cue IDs,
        and other VTT formatting while preserving
        the actual transcript text.
    """

    extension = os.path.splitext(filename)[1].lower()

    if extension not in [".txt", ".vtt"]:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Please provide a .txt or .vtt file."
        )

    with open(filename, "r", encoding="utf-8-sig") as file:
        content = file.read()

    # TXT files don't require any parsing
    if extension == ".txt":
        return content.strip()

    # -----------------------------------------------------
    # VTT processing
    # -----------------------------------------------------

    lines = content.splitlines()

    transcript_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip WebVTT header
        if line.startswith("WEBVTT"):
            continue

        # Skip VTT metadata/header lines
        if line.startswith(("NOTE", "STYLE", "REGION")):
            continue

        # Skip timestamps
        # Example:
        # 00:00:01.000 --> 00:00:05.000
        if "-->" in line:
            continue

        # Skip numeric cue IDs
        # Example:
        # 1
        # 2
        if re.fullmatch(r"\d+", line):
            continue

        # Remove common VTT formatting tags
        line = re.sub(r"</?[^>]+>", "", line)

        # Convert HTML entities if present
        line = (
            line.replace("&nbsp;", " ")
                .replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
        )

        if line:
            transcript_lines.append(line)

    return "\n".join(transcript_lines).strip()


# ---------------------------------------------------------
# Step 1: Read the meeting transcript
# ---------------------------------------------------------

class ReadTranscript(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def read_file(
        self,
        filename: str,
        ctx: WorkflowContext[str],
    ) -> None:

        transcript = read_transcript_file(filename)

        if not transcript:
            raise ValueError(
                f"No transcript content found in file: {filename}"
            )

        await ctx.send_message(transcript)


# ---------------------------------------------------------
# Step 2: Summarize using the Foundry model
# ---------------------------------------------------------

class SummarizeMeeting(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def summarize(
        self,
        transcript: str,
        ctx: WorkflowContext[str],
    ) -> None:

        prompt = f"""
Summarize the following meeting transcript.

Meeting transcript:
---
{transcript}
---

Produce a concise daily standup summary with:

1. Key Updates
2. Decisions
3. Blockers
4. Action Items

Do not invent information that is not explicitly present
in the transcript.
"""

        response = await summarizer_agent.run(prompt)

        summary = str(response)

        await ctx.send_message(summary)


# ---------------------------------------------------------
# Step 3: Produce the final workflow output
# ---------------------------------------------------------

class GenerateStandup(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def generate(
        self,
        summary: str,
        ctx: WorkflowContext[Never, str],
    ) -> None:

        await ctx.yield_output(summary)


# ---------------------------------------------------------
# Build workflow
# ---------------------------------------------------------

def create_workflow():
    reader = ReadTranscript(id="read_transcript")
    summarizer = SummarizeMeeting(id="summarize_meeting")
    standup = GenerateStandup(id="generate_standup")

    return (
        WorkflowBuilder(start_executor=reader)
        .add_edge(reader, summarizer)
        .add_edge(summarizer, standup)
        .build()
    )


# ---------------------------------------------------------
# Run workflow
# ---------------------------------------------------------

async def main():
    workflow = create_workflow()

    # Can now be either:
    # meeting_transcript.txt
    # meeting_transcript.vtt
    filename = "meeting_transcript.vtt"

    events = await workflow.run(filename)

    print("Daily Standup:")
    print(events.get_outputs()[0])


if __name__ == "__main__":
    asyncio.run(main())
