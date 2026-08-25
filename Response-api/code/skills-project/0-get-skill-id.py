"""
export MY_FOUNDRY_ENDPOINT="https://project-01-us.services.ai.azure.com/api/projects/14juneproject"
echo $MY_FOUNDRY_ENDPOINT
nano 1.py
python -m venv venv 
source venv/bin/activate
pip install azure-ai-projects azure-identity
python 1.py 
"""

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://foundry0309.services.ai.azure.com/api/projects/proj-default"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # List all skills in the project
    skills = list(project.beta.skills.list())
    print(f"Found {len(skills)} skill(s)")
    for skill in skills:
        print(f"{skill.name} has ID: {skill.id } (default: {skill.default_version})")