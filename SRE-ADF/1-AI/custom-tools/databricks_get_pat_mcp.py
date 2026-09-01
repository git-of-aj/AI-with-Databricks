import os

import requests
from dotenv import load_dotenv


load_dotenv(
    r"C:\Users\anana\Downloads\AI-with-Databricks\SRE-ADF\1-AI\.env"
)

DATABRICKS_HOST = (
    "https://adb-7405619671541936.16.azuredatabricks.net"
).rstrip("/")


def fetch_databricks_pat_details():
    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

    if not client_id:
        raise ValueError("DATABRICKS_CLIENT_ID is missing from .env")

    if not client_secret:
        raise ValueError("DATABRICKS_CLIENT_SECRET is missing from .env")

    # Get OAuth access token
    token_url = f"{DATABRICKS_HOST}/oidc/v1/token"

    token_response = requests.post(
        token_url,
        auth=(client_id, client_secret),
        data={
            "grant_type": "client_credentials",
            "scope": "all-apis",
        },
        timeout=30,
    )

    if not token_response.ok:
        raise RuntimeError(
            f"OAuth token request failed: "
            f"{token_response.status_code} "
            f"{token_response.text}"
        )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise RuntimeError(
            f"No access_token returned by Databricks: {token_data}"
        )

    # Call Databricks Token Management API
    url = f"{DATABRICKS_HOST}/api/2.0/token-management/tokens"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"Databricks API request failed: "
            f"{response.status_code} "
            f"{response.text}"
        )

    data = response.json()

    return data.get("token_infos", [])