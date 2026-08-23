import os
from pydantic import BaseModel
from template import get_openai_client

client = get_openai_client()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

def completion():
    completion = client.beta.chat.completions.parse(
        model="gpt-5-mini", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
        ],
        response_format=CalendarEvent,
    )

    event = completion.choices[0].message.parsed

    print(event)
    print(completion.model_dump_json(indent=2))