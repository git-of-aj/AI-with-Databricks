from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import requests
import json

load_dotenv()

app = FastAPI()

credential = DefaultAzureCredential()


def get_failed_adf_activities(api_url: str):
    """
    Call Azure Log Analytics API using the URL received
    from Azure Monitor alert.
    """

    token = credential.get_token(
        "https://api.loganalytics.io/.default"
    )

    response = requests.get(
        api_url,
        headers={
            "Authorization": f"Bearer {token.token}",
            "Prefer": "include-permissions=true",
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data


def format_adf_failures(data):
    """
    Convert Log Analytics response into simple JSON.
    """

    results = []

    # Azure Log Analytics returns:
    # {
    #   "tables": [
    #       {
    #           "columns": [...],
    #           "rows": [...]
    #       }
    #   ]
    # }

    if not data.get("tables"):
        return results

    table = data["tables"][0]

    columns = [
        column["name"]
        for column in table.get("columns", [])
    ]

    rows = table.get("rows", [])

    for row in rows:
        record = dict(zip(columns, row))

        results.append({
            "pipeline": record.get("PipelineName"),
            "activity": record.get("ActivityName"),
            "activityType": record.get("ActivityType"),
            "status": "Failed",
            "failureTime": record.get("TimeGenerated"),
            "errorMessage": record.get("ErrorMessage"),
            "error": record.get("Error"),
            "resourceId": record.get("ResourceId"),
        })

    return results


@app.post("/azure-alert")
async def azure_alert(request: Request):

    # ---------------------------------------------------------
    # 1. Receive Azure Monitor webhook
    # ---------------------------------------------------------

    payload = await request.json()

    print("\n" + "=" * 80)
    print("AZURE MONITOR ALERT RECEIVED")
    print("=" * 80)

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    print("=" * 80)

    # ---------------------------------------------------------
    # 2. Extract linkToFilteredSearchResultsAPI
    # ---------------------------------------------------------

    link_to_api = None

    try:
        link_to_api = (
            payload
            .get("data", {})
            .get("essentials", {})
            .get("linkToFilteredSearchResultsAPI")
        )
    except Exception:
        pass

    if not link_to_api:
        return {
            "status": "error",
            "message": "linkToFilteredSearchResultsAPI not found in alert payload"
        }

    print("\nLog Analytics API URL:")
    print(link_to_api)

    # ---------------------------------------------------------
    # 3. Call Log Analytics API
    # ---------------------------------------------------------

    try:

        log_data = get_failed_adf_activities(link_to_api)

    except requests.exceptions.HTTPError as e:

        return {
            "status": "error",
            "message": "Log Analytics API request failed",
            "details": str(e),
        }

    except Exception as e:

        return {
            "status": "error",
            "message": "Unexpected error",
            "details": str(e),
        }

    # ---------------------------------------------------------
    # 4. Convert response into simple JSON
    # ---------------------------------------------------------

    failures = format_adf_failures(log_data)

    # ---------------------------------------------------------
    # 5. Pretty-print result
    # ---------------------------------------------------------

    result = {
        "status": "success",
        "failedActivityCount": len(failures),
        "failures": failures,
    }

    print("\n" + "=" * 80)
    print("ADF FAILURE SUMMARY")
    print("=" * 80)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )

    print("=" * 80 + "\n")

    return result


@app.get("/", response_class=HTMLResponse)
async def home():

    return """
    <h1>Azure Monitor Webhook</h1>

    <p>
        POST Azure Monitor alerts to
        <code>/azure-alert</code>
    </p>
    """
