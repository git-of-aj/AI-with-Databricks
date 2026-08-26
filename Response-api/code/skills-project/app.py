import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

ENDPOINT = "https://project-01-us.openai.azure.com/openai/v1"
MODEL = "gpt-5.4-mini"
API_KEY = os.getenv("MY_KEY")

SKILL_ID = "skill_eecae3cab6e31b2c23b46f6ceb7f5d8aa2aef075" # RCA_ANALYZER

LOG_FILE = r"C:\Users\Ananay.Ojha\Downloads\AI-with-Databricks\Response-api\code\skills-project\sample.log"


# ---------------------------------------------------------
# Azure authentication
# ---------------------------------------------------------


client = OpenAI(
        base_url=ENDPOINT,
        api_key=API_KEY,
)

# -------------- Pre-Req ------------
def upload_file():
    with open("sample-app.log", "rb") as f:
        uploaded_file = client.files.create(
            file=f,
            purpose="user_data",
        )

    print(f"{LOG_FILE} file uploaded with ID: {uploaded_file.id}")
    return uploaded_file.id

file_id = upload_file()
# ---------------------------------------------------------
# RCA request
# ---------------------------------------------------------

environment = """
Application: payments-api
Environment: production
Platform: Azure Kubernetes Service (AKS)
Ingress: Azure Application Gateway
Runtime: Python 3.12
Database: PostgreSQL
Region: West Europe
"""

prompt = f"""
You are investigating a production incident.

Use the rca-log-analyzer skill.

The supplied log file is:

{LOG_FILE}

Application environment:

{environment}

Perform the RCA workflow:

1. Inspect the log file using the hosted shell.
2. Run the Skill's log analyzer script.
3. Identify important errors, exceptions, warnings and HTTP status codes.
4. Search the web for important error codes and relevant official documentation.
5. Correlate the search results with the application environment.
6. Determine the most likely root causes.
7. Provide practical remediation steps.

Important:

- Do not modify anything.
- Do not restart anything.
- Do not execute deployment commands.
- Do not expose secrets.
- Treat the logs as the primary evidence.
- Clearly distinguish facts from hypotheses.
- Cite web sources when you use web-search information.
"""


# ---------------------------------------------------------
# Responses API
# ---------------------------------------------------------

response = client.responses.create(
    model=MODEL,

    tools=[
        {
            "type": "shell",
            "environment": {
                "type": "container_auto",
                "skills": [
                    {
                        "type": "skill_reference",
                        "skill_id": SKILL_ID,
                    }
                ],
            },
        },
        {
            "type": "web_search",
        },
    ],

    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt,
                },
                {
                    "type": "input_file",
                    "file_id": file_id,
                },
            ],
        }
    ],
)


print("\n")
print("=" * 70)
print("ROOT CAUSE ANALYSIS")
print("=" * 70)
print()

print(response.output_text)
