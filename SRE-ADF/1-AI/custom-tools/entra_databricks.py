import os
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient

# Load .env
load_dotenv(
    r"C:\Users\anana\Downloads\AI-with-Databricks\SRE-ADF\1-AI\.env"
)

# Azure App Registration / Microsoft Entra credentials
tenant_id = os.getenv("ARM_TENANT_ID")
client_id = os.getenv("ARM_CLIENT_ID")
client_secret = os.getenv("ARM_CLIENT_SECRET")

# Azure Databricks workspace
host = os.getenv("DATABRICKS_HOST")

# Create Databricks client
w = WorkspaceClient(
    host=host,
    azure_tenant_id=tenant_id,
    azure_client_id=client_id,
    azure_client_secret=client_secret,
)

# Test authentication
user = w.current_user.me()

print("Authentication successful!")
print("Databricks user:", user.user_name)
