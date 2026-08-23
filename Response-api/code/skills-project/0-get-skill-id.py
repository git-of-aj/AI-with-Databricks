"""
 5  export MY_FOUNDRY_ENDPOINT="https://project-01-us.services.ai.azure.com/api/projects/14juneproject"
    6  echo MY_FOUNDRY_ENDPOINT
    7  echo $MY_FOUNDRY_ENDPOINT
    8  nano 1.py
    9  python -m venv venv 
   10  source venv/bin/activate
   11  pip install azure-ai-projects azure-identity
   12  python 1.py 
   13  history
"""


import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["MY_FOUNDRY_ENDPOINT"]

with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
    allow_preview=True,
) as project:

    skills = list(project.beta.skills.list())

    for skill in skills:
        print(f"Name: {skill.name}")
        print(f"Skill ID: {skill.id}")
        print(f"Default version: {skill.default_version}")
        print()
