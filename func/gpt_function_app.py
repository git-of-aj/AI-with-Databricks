import json
import logging
import azure.functions as func

app = func.FunctionApp()

@app.route(
    route="process_adf_failure",
    methods=["POST"],
    auth_level=func.AuthLevel.FUNCTION
)
def process_adf_failure(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("ADF failure alert received.")

    try:
        payload = req.get_json()

        data = payload.get("data", {})
        essentials = data.get("essentials", {})
        alert_context = data.get("alertContext", {})

        # ---------------------------------------------------------
        # 1. Date and Time
        # ---------------------------------------------------------
        date_time = (
            essentials.get("firedDateTime")
            or alert_context.get("SearchIntervalEndTimeUtc")
            or ""
        )

        # ---------------------------------------------------------
        # 2. Try to obtain search results
        # ---------------------------------------------------------
        rows = []
        search_results = alert_context.get("SearchResults", {})
        tables = search_results.get("tables", [])

        if tables:
            table = tables[0]
            columns = [
                column.get("name")
                for column in table.get("columns", [])
            ]

            for row in table.get("rows", []):
                rows.append(dict(zip(columns, row)))

        # ---------------------------------------------------------
        # 3. Extract ADF fields
        # ---------------------------------------------------------
        result = rows[0] if rows else {}

        resource_id = (
            result.get("_ResourceId")
            or result.get("ResourceId")
            or ""
        )

        subscription = (
            result.get("_SubscriptionId")
            or extract_subscription(resource_id)
            or ""
        )

        resource_group = extract_resource_group(resource_id)

        resource_name = (
            result.get("PipelineName")
            or extract_factory_name(resource_id)
            or ""
        )

        error_code = result.get("ErrorCode", "")
        error_message = result.get("ErrorMessage", "")
        failure_type = result.get("FailureType", "")
        run_id = result.get("RunId", "")

        error_details = {
            "PipelineName": result.get("PipelineName", ""),
            "RunId": run_id,
            "ErrorCode": error_code,
            "ErrorMessage": error_message,
            "FailureType": failure_type
        }

        output = {
            "Date and Time": date_time,
            "Resource_Name": resource_name,
            "Resource_Group": resource_group,
            "Susbcription": subscription,
            "Error_Details": error_details
        }

        return func.HttpResponse(
            json.dumps(output, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as exc:
        logging.exception("Error processing ADF failure alert")

        return func.HttpResponse(
            json.dumps({
                "error": str(exc)
            }),
            status_code=500,
            mimetype="application/json"
        )


def extract_subscription(resource_id: str) -> str:
    parts = resource_id.strip("/").split("/")
    try:
        index = parts.index("subscriptions")
        return parts[index + 1]
    except (ValueError, IndexError):
        return ""


def extract_resource_group(resource_id: str) -> str:
    parts = resource_id.strip("/").split("/")
    try:
        index = parts.index("resourceGroups")
        return parts[index + 1]
    except (ValueError, IndexError):
        return ""


def extract_factory_name(resource_id: str) -> str:
    parts = resource_id.strip("/").split("/")
    try:
        index = parts.index("factories")
        return parts[index + 1]
    except (ValueError, IndexError):
        return ""
