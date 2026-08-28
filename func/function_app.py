import logging
import azure.functions as func

# Initialize the Function App with Anonymous access level for the webhook
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="process_adf_failure", methods=["POST"])
def process_azure_alert(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function starting to process an Azure Monitor Alert request.")

    try:
        # Parse the incoming JSON payload
        req_body = req.get_json()
        
        # Extract the schema id to verify it's an Azure Monitor Alert
        schema_id = req_body.get("schemaId")
        
        if schema_id == "azureMonitorCommonAlertSchema":
            data = req_body.get("data", {})
            essentials = data.get("essentials", {})
            
            # Extract critical alert details
            alert_name = essentials.get("alertRule")
            severity = essentials.get("severity")
            signal_type = essentials.get("signalType")
            alert_target = essentials.get("targetResourceName")
            description = essentials.get("description")
            
            logging.info(f"🚨 New Alert Received: {alert_name}")
            logging.info(f"Severity: {severity} | Target: {alert_target} | Type: {signal_type}")
            logging.info(f"Description: {description}")
            
            # TODO: Add your custom logic here (e.g., send to Slack, log to database, trigger auto-remediation)
            
            return func.HttpResponse(
                "Alert processed successfully.",
                status_code=200
            )
        else:
            logging.warning(f"Received unknown schema: {schema_id}")
            return func.HttpResponse(
                "Unsupported alert schema. Please use the Common Alert Schema.",
                status_code=400
            )

    except ValueError:
        logging.error("Invalid JSON payload received.")
        return func.HttpResponse(
            "Invalid JSON body.",
            status_code=400
        )
    except Exception as e:
        logging.error(f"Error processing alert: {str(e)}")
        return func.HttpResponse(
            "Internal server error processing alert.",
            status_code=500
        )
