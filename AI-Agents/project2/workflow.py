import asyncio
import os
from dotenv import load_dotenv
load_dotenv('../.env')

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

        with open(filename, "r", encoding="utf-8") as file:
            transcript = file.read()

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
"""

        response = await summarizer_agent.run(prompt)

        # Agent responses can be converted to string
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

    events = await workflow.run("meeting_transcript.txt")

    print("Daily Standup:")
    print(events.get_outputs()[0])


if __name__ == "__main__":
    asyncio.run(main())
