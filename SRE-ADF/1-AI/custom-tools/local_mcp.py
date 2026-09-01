from fastmcp import FastMCP
from specific_linked_service import adf_get_linked_srv

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


if __name__ == "__main__":
    mcp.run()
