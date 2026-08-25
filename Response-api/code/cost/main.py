import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("MY_ENDPOINT")
api_key = os.getenv("MY_KEY")

client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
    )

skill = Path("SKILL.md").read_text()
scripts = "\n\n".join(
    f"--- {p} ---\n{p.read_text()}"
    for p in Path("scripts").glob("*")
    if p.is_file()
)

response = client.responses.create(
    model="gpt-5.4-mini",
    instructions=skill,
    input=f"""
{scripts}

Execute the skill according to SKILL.md.
""",
)

print(response.output_text)
