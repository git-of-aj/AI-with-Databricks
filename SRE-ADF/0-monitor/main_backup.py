from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import requests
import json
import hashlib

load_dotenv()

app = FastAPI()

credential = DefaultAzureCredential()

# Store the latest processed ADF alerts in memory.
# Key = generated unique ID
# Value = final alert result
adf_alerts = {}


def generate_resource_id(resource_id: str) -> str:
    """
    Generate a stable unique ID based on the Azure resource ID.

    The same resourceId will always generate the same ID.
    """

    if not resource_id:
        return "unknown-resource"

    return hashlib.sha256(
        resource_id.encode("utf-8")
    ).hexdigest()[:16]


def get_log_analytics_data(api_url: str):
    """
    Call the Log Analytics API using the URL
    provided by Azure Monitor.
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

    print("\nLOG ANALYTICS HTTP STATUS:", response.status_code)

    print("\nRAW LOG ANALYTICS RESPONSE:")
    print(response.text)

    response.raise_for_status()

    return response.json()


def extract_error_details(record):
    """
    Try to get the most useful error information from ADF.
    """

    error_message = record.get("ErrorMessage")
    error = record.get("Error")
    output = record.get("Output")

    if error_message:
        return error_message

    if error:

        if isinstance(error, str):

            try:
                error_json = json.loads(error)

                if isinstance(error_json, dict):

                    return (
                        error_json.get("message")
                        or error_json.get("Message")
                        or error
                    )

            except Exception:
                pass

        return error

    if output:

        if isinstance(output, str):

            try:
                output_json = json.loads(output)

                if isinstance(output_json, dict):

                    if "error" in output_json:

                        error_data = output_json["error"]

                        if isinstance(error_data, dict):
                            return (
                                error_data.get("message")
                                or error_data.get("Message")
                                or json.dumps(error_data)
                            )

                        return str(error_data)

                    if "errors" in output_json:
                        return json.dumps(
                            output_json["errors"],
                            ensure_ascii=False
                        )

                    if "message" in output_json:
                        return output_json["message"]

            except Exception:
                pass

        return output

    return "No error details returned"


def format_adf_failures(data):
    """
    Convert Azure Log Analytics response into
    simple readable JSON.
    """

    results = []

    tables = data.get("tables", [])

    if not tables:
        return results

    table = tables[0]

    columns = [
        column["name"]
        for column in table.get("columns", [])
    ]

    rows = table.get("rows", [])

    print("\nLOG ANALYTICS COLUMNS:")
    print(columns)

    print("\nNUMBER OF ROWS:")
    print(len(rows))

    for row in rows:

        record = dict(zip(columns, row))

        print("\nADF ACTIVITY RECORD:")
        print(
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False
            )
        )

        resource_id = record.get("ResourceId")

        unique_id = generate_resource_id(
            resource_id
        )

        results.append({
            "id": unique_id,
            "pipeline": record.get("PipelineName"),
            "activity": record.get("ActivityName"),
            "activityType": record.get("ActivityType"),
            "status": record.get("Status", "Failed"),
            "failureTime": record.get("TimeGenerated"),
            "errorDetails": extract_error_details(record),
            "resourceId": resource_id,
        })

    return results


@app.post("/azure-alert")
async def azure_alert(request: Request):

    # =========================================================
    # 1. RECEIVE AZURE MONITOR ALERT
    # =========================================================

    payload = await request.json()

    print("\n" + "=" * 80)
    print("AZURE MONITOR ALERT RECEIVED")
    print("=" * 80)

    print(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False
        )
    )

    print("=" * 80)

    # =========================================================
    # 2. EXTRACT FILTERED LOG ANALYTICS API URL
    # =========================================================

    try:

        link_to_api = (
            payload
            ["data"]
            ["alertContext"]
            ["condition"]
            ["allOf"][0]
            ["linkToFilteredSearchResultsAPI"]
        )

    except (KeyError, IndexError, TypeError):

        return {
            "status": "error",
            "message": "linkToFilteredSearchResultsAPI not found"
        }

    print("\n" + "=" * 80)
    print("FILTERED LOG ANALYTICS API")
    print("=" * 80)

    print(link_to_api)

    # =========================================================
    # 3. CALL LOG ANALYTICS
    # =========================================================

    try:

        log_data = get_log_analytics_data(
            link_to_api
        )

    except requests.exceptions.HTTPError as e:

        return {
            "status": "error",
            "message": "Log Analytics API returned an HTTP error",
            "details": str(e),
        }

    except Exception as e:

        return {
            "status": "error",
            "message": "Failed to query Log Analytics",
            "details": str(e),
        }

    # =========================================================
    # 4. FORMAT ADF FAILURE DATA
    # =========================================================

    failures = format_adf_failures(
        log_data
    )

    # =========================================================
    # 5. SAVE FINAL RESULTS
    # =========================================================

    for failure in failures:

        alert_id = failure["id"]

        adf_alerts[alert_id] = failure

    # =========================================================
    # 6. FINAL JSON RESPONSE
    # =========================================================

    result = {
        "status": "success",
        "failedActivityCount": len(failures),
        "failures": failures,
    }

    print("\n" + "=" * 80)
    print("FINAL ADF FAILURE SUMMARY")
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


@app.get("/adf/alerts")
async def get_adf_alerts():
    """
    Return all processed ADF alerts.
    """

    result = {
        "status": "success",
        "count": len(adf_alerts),
        "alerts": list(adf_alerts.values()),
    }

    print("\n" + "=" * 80)
    print("GET /adf/alerts")
    print("=" * 80)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
(venv) aj@test78:~$ cat 2_main.py 
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import requests
import json

load_dotenv()

app = FastAPI()

credential = DefaultAzureCredential()


def get_log_analytics_data(api_url: str):
    """
    Call the Log Analytics API using the URL
    provided by Azure Monitor.
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

    print("\nLOG ANALYTICS HTTP STATUS:", response.status_code)

    # Print raw response for troubleshooting
    print("\nRAW LOG ANALYTICS RESPONSE:")
    print(response.text)

    response.raise_for_status()

    return response.json()


def extract_error_details(record):
    """
    Try to get the most useful error information from ADF.
    """

    error_message = record.get("ErrorMessage")
    error = record.get("Error")
    output = record.get("Output")

    # ---------------------------------------------------------
    # If ErrorMessage exists, use it
    # ---------------------------------------------------------

    if error_message:
        return error_message

    # ---------------------------------------------------------
    # Try Error column
    # ---------------------------------------------------------

    if error:

        # Error can sometimes be a JSON string
        if isinstance(error, str):

            try:
                error_json = json.loads(error)

                if isinstance(error_json, dict):

                    return (
                        error_json.get("message")
                        or error_json.get("Message")
                        or error
                    )

            except Exception:
                pass

        return error

    # ---------------------------------------------------------
    # Try Output column
    # ---------------------------------------------------------

    if output:

        if isinstance(output, str):

            try:
                output_json = json.loads(output)

                if isinstance(output_json, dict):

                    # Common possible locations
                    if "error" in output_json:

                        error_data = output_json["error"]

                        if isinstance(error_data, dict):
                            return (
                                error_data.get("message")
                                or error_data.get("Message")
                                or json.dumps(error_data)
                            )

                        return str(error_data)

                    if "errors" in output_json:
                        return json.dumps(
                            output_json["errors"],
                            ensure_ascii=False
                        )

                    if "message" in output_json:
                        return output_json["message"]

            except Exception:
                pass

        return output

    return "No error details returned"


def format_adf_failures(data):
    """
    Convert Azure Log Analytics response into
    simple readable JSON.
    """

    results = []

    tables = data.get("tables", [])

    if not tables:
        return results

    table = tables[0]

    columns = [
        column["name"]
        for column in table.get("columns", [])
    ]

    rows = table.get("rows", [])

    print("\nLOG ANALYTICS COLUMNS:")
    print(columns)

    print("\nNUMBER OF ROWS:")
    print(len(rows))

    for row in rows:

        record = dict(zip(columns, row))

        # Print one complete record so we can see
        # exactly where ADF is putting the error.
        print("\nADF ACTIVITY RECORD:")
        print(
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False
            )
        )

        results.append({
            "pipeline": record.get("PipelineName"),
            "activity": record.get("ActivityName"),
            "activityType": record.get("ActivityType"),
            "status": record.get("Status", "Failed"),
            "failureTime": record.get("TimeGenerated"),
            "errorDetails": extract_error_details(record),
            "resourceId": record.get("ResourceId"),
        })

    return results


@app.post("/azure-alert")
async def azure_alert(request: Request):

    # =========================================================
    # 1. RECEIVE AZURE MONITOR ALERT
    # =========================================================

    payload = await request.json()

    print("\n" + "=" * 80)
    print("AZURE MONITOR ALERT RECEIVED")
    print("=" * 80)

    print(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False
        )
    )

    print("=" * 80)

    # =========================================================
    # 2. EXTRACT FILTERED LOG ANALYTICS API URL
    # =========================================================

    try:

        link_to_api = (
            payload
            ["data"]
            ["alertContext"]
            ["condition"]
            ["allOf"][0]
            ["linkToFilteredSearchResultsAPI"]
        )

    except (KeyError, IndexError, TypeError):

        return {
            "status": "error",
            "message": "linkToFilteredSearchResultsAPI not found"
        }

    print("\n" + "=" * 80)
    print("FILTERED LOG ANALYTICS API")
    print("=" * 80)

    print(link_to_api)

    # =========================================================
    # 3. CALL LOG ANALYTICS
    # =========================================================

    try:

        log_data = get_log_analytics_data(
            link_to_api
        )

    except requests.exceptions.HTTPError as e:

        return {
            "status": "error",
            "message": "Log Analytics API returned an HTTP error",
            "details": str(e),
        }

    except Exception as e:

        return {
            "status": "error",
            "message": "Failed to query Log Analytics",
            "details": str(e),
        }

    # =========================================================
    # 4. FORMAT ADF FAILURE DATA
    # =========================================================

    failures = format_adf_failures(
        log_data
    )

    # =========================================================
    # 5. FINAL JSON RESPONSE
    # =========================================================

    result = {
        "status": "success",
        "failedActivityCount": len(failures),
        "failures": failures,
    }

    print("\n" + "=" * 80)
    print("FINAL ADF FAILURE SUMMARY")
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