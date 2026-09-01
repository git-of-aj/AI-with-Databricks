import os
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient


# ============================================================
# Load .env
# ============================================================

load_dotenv(
    r"C:\Users\anana\Downloads\AI-with-Databricks\SRE-ADF\1-AI\.env",
    override=True
)


# ============================================================
# Azure App Registration / Microsoft Entra credentials
# ============================================================

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("CLIENT")
client_secret = os.getenv("SECRET")

host = os.getenv("DATABRICKS_HOST")


# ============================================================
# Remove conflicting Databricks OAuth environment variables
# ============================================================

os.environ.pop("DATABRICKS_CLIENT_ID", None)
os.environ.pop("DATABRICKS_CLIENT_SECRET", None)


# ============================================================
# Validate configuration
# ============================================================

if not tenant_id:
    raise ValueError("AZURE_TENANT_ID is missing")

if not client_id:
    raise ValueError("AZURE_CLIENT_ID is missing")

if not client_secret:
    raise ValueError("AZURE_CLIENT_SECRET is missing")

if not host:
    raise ValueError("DATABRICKS_HOST is missing")


print("Databricks host:", host)
print("Azure tenant:", tenant_id)
print("Azure client ID:", client_id)


# ============================================================
# Create Databricks client using Azure authentication
# ============================================================

w = WorkspaceClient(
    host=host,
    azure_tenant_id=tenant_id,
    azure_client_id=client_id,
    azure_client_secret=client_secret,
)

# ============================================================
# Test authentication
# ============================================================

user = w.current_user.me()

print("\nAuthentication successful!")
print("Databricks user:", user.user_name)
