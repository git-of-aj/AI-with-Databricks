import os
import json
import requests

from azure.identity import ClientSecretCredential
from dotenv import load_dotenv


# Load variables from .env
load_dotenv(
    r"C:\Users\anana\Downloads\AI-with-Databricks\SRE-ADF\1-AI\.env"
)

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")


# Authenticate using Service Principal credentials
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)


def adf_get_linked_srv(resource_id: str) -> str:
    """
    Retrieve a specific Azure Data Factory linked service.

    Args:
        resource_id: Full Azure Resource Manager resource ID.

    Returns:
        Linked service details as a formatted JSON string.
    """

    # Get a fresh Azure Management API token
    token = credential.get_token(
        "https://management.azure.com/.default"
    )

    url = (
        f"https://management.azure.com/"
        f"{resource_id}?api-version=2018-06-01"
    )

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # Return the result to the MCP server / AI
    return json.dumps(data, indent=2)
