# from template import get_openai_client

# client = get_openai_client()

# config/openai_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("MY_ENDPOINT")
api_key = os.getenv("MY_KEY")

client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
    )


# Run a command in an auto-provisioned hosted container.
response = client.responses.create(
    model="gpt-5.4-mini",
    tools=[{"type": "shell", "environment": {"type": "container_auto"}}],
    input="Run: python --version && echo 'hello from the shell'",
)

print(response.output_text)