from fastmcp import FastMCP
from specific_linked_service import adf_get_linked_srv
from databricks_get_pat_mcp import fetch_databricks_pat_details
import json

mcp = FastMCP("Current State Validator")

@mcp.tool
def azure_data_factory_linked_service(resource_id: str) -> str:
    """
    Get the details of a specific Azure Data Factory linked service.

    Use this tool when the user wants to retrieve the configuration/details
    of a specific linked service in Azure Data Factory.

    The resource_id must be the complete Azure Resource Manager resource ID
    of the linked service, for example:

    /subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/
    Microsoft.DataFactory/factories/{factory-name}/linkedservices/{linked-service-name}

    Args:
        resource_id: Full Azure Resource Manager resource ID of the ADF
                     linked service.

    Returns:
        The linked service details as a JSON string.
    """
    try:
        result = adf_get_linked_srv(resource_id)
        return result

    except Exception as e:
        return f"Error retrieving Azure Data Factory linked service: {str(e)}"

@mcp.tool
def get_databricks_pat_details() -> str:
    """
    Retrieve metadata for personal access tokens (PATs) configured in an
    Azure Databricks workspace.

    Use this tool when the user needs to inspect or audit Databricks PAT
    information, such as token ID, creator, comment, scopes, workspace ID,
    owner ID, creation time, expiry time, or last-used time.

    Authentication is performed using Databricks OAuth machine-to-machine
    (M2M) credentials configured in the databricks environment via databricks service principal. 
    The actual PAT secret values are never returned.

    Arguments:
        None.

    Returns:
        A JSON string containing the list of Databricks PAT metadata objects.
        The response does not contain the actual PAT secret/token values.

    Raises:
        Exception: If OAuth authentication fails, required environment
        variables are missing, or the Databricks Token Management API request
        fails.
    """
    try:
        result = fetch_databricks_pat_details()
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps(
            {"error": f"Error retrieving Databricks PAT details: {str(e)}"},
            indent=2,
        )

if __name__ == "__main__":
    mcp.run()
