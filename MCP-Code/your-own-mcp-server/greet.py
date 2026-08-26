from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text, Badge, Row
from fastmcp import FastMCP

mcp = FastMCP("Greeting Server")


@mcp.tool(app=True)
def greet(name: str) -> PrefabApp:
    """
    Description: Use this tool to every greeting message from user like Hi, Hello, hey there
    Args: Ask for user Name 
    Returns: a PrefabApp saying Hello, Nice to meet you {name}
    """
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Hello, Nice to meet you {name}!")
        with Row(gap=2, align="center"):
            Text("Status")
            Badge("Greeted", variant="success")

    return PrefabApp(view=view)

if __name__ == "__main__":
    mcp.run()