import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


# ============================================================
# Load variables from .env
# ============================================================

load_dotenv(
    r"C:\Users\anana\Downloads\AI-with-Databricks\SRE-ADF\1-AI\.env"
)

# IMPORTANT:
# These must be the Databricks service principal credentials:
#
# DATABRICKS_CLIENT_ID     = Databricks service principal client ID
# DATABRICKS_CLIENT_SECRET = Databricks OAuth secret
#
# Do NOT use an Azure/Entra client secret here if you are
# trying to use Databricks OAuth M2M.

client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

DATABRICKS_HOST = (
    "https://adb-7405619671541936.16.azuredatabricks.net"
)


# ============================================================
# Validate configuration
# ============================================================

if not client_id:
    raise ValueError(
        "DATABRICKS_CLIENT_ID is missing from .env"
    )

if not client_secret:
    raise ValueError(
        "DATABRICKS_CLIENT_SECRET is missing from .env"
    )


# Remove a trailing slash if one was accidentally added
DATABRICKS_HOST = DATABRICKS_HOST.rstrip("/")


# ============================================================
# Get Databricks OAuth M2M access token
# ============================================================
#
# For workspace-level OAuth M2M authentication, Databricks
# documents this endpoint:
#
# https://<workspace-host>/oidc/v1/token
#
# The OAuth secret is sent using HTTP Basic Authentication.
#

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
    print("OAuth token request failed")
    print("HTTP status:", token_response.status_code)
    print("Response:", token_response.text)
    token_response.raise_for_status()

token_data = token_response.json()

access_token = token_data.get("access_token")

if not access_token:
    raise RuntimeError(
        f"No access_token returned by Databricks: {token_data}"
    )

print("Successfully obtained Databricks OAuth access token.")


# ============================================================
# Call Databricks Token Management API
# ============================================================

def get_databricks_pat_details():

    url = f"{DATABRICKS_HOST}/api/2.0/token-management/tokens"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )


    # ============================================================
    # Error handling
    # ============================================================

    if not response.ok:
        print("Databricks API request failed")
        print("HTTP status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()


    # ============================================================
    # Parse response
    # ============================================================

    data = response.json()

    token_infos = data.get("token_infos", [])

    if not token_infos:
        print("No token information returned.")
    else:
        for token_info in token_infos:

            print("=" * 60)

            print(
                "Token ID:        ",
                token_info.get("token_id")
            )

            print(
                "Created by:      ",
                token_info.get("created_by_username")
            )

            print(
                "Comment:         ",
                token_info.get("comment")
            )

            print(
                "Scopes:          ",
                token_info.get("scopes")
            )

            print(
                "Workspace ID:    ",
                token_info.get("workspace_id")
            )

            print(
                "Owner ID:        ",
                token_info.get("owner_id")
            )

            # ----------------------------------------------------
            # Creation time
            # ----------------------------------------------------

            creation = token_info.get("creation_time")

            if creation:
                print(
                    "Created:         ",
                    datetime.fromtimestamp(
                        creation / 1000,
                        timezone.utc
                    )
                )

            # ----------------------------------------------------
            # Expiry time
            # ----------------------------------------------------

            expiry = token_info.get("expiry_time")

            if expiry:
                print(
                    "Expires:         ",
                    datetime.fromtimestamp(
                        expiry / 1000,
                        timezone.utc
                    )
                )

            # ----------------------------------------------------
            # Last used
            # ----------------------------------------------------

            last_used = token_info.get("last_used_day")

            if last_used:
                print(
                    "Last used:       ",
                    datetime.fromtimestamp(
                        last_used / 1000,
                        timezone.utc
                    )
                )
