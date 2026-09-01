import os
import requests
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
import json

# Load variables from .env
load_dotenv(r"C:\Users\anana\Downloads\AI-with-Databricks\SRE-ADF\1-AI\.env")

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
resource_id = "/subscriptions/99d8f8e9-1b37-4b2d-b102-416a5bc55c43/resourceGroups/adf/providers/Microsoft.DataFactory/factories/adf-01-ind-01/linkedservices/AzureDatabricks"
sub_service = "linkedservices"


#Authenticate using Service Principal credentials
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Get Azure Management API token
token = credential.get_token(
    "https://management.azure.com/.default"
)

def adf_get_linked_srv(resource_id): 
    url = (
    f"https://management.azure.com/{resource_id}?api-version=2018-06-01"
)
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }
    )

    response.raise_for_status()

    data = response.json()

    print(json.dumps(data, indent=2))
