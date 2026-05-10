"""
FastMCP quickstart example.

Run from the repository root:
    uv run main.py
"""

from datetime import date
import traceback

from mcp.server.fastmcp import FastMCP
from pydantic_monty import Monty, CollectString, MontyError

# Create an MCP server
mcp = FastMCP("localai-python-mcp", json_response=True)

@mcp.tool()
def exec(cmd: str) -> str:
    """Execute python code and return the result."""
    try:
        output_collector = CollectString()
        monty = Monty(cmd)
        monty.run(print_callback=output_collector)
        return output_collector.output
    except MontyError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {traceback.format_exc()}"

@mcp.tool()
def get_date() -> str:
    """Get current date."""
    today = date.today()
    day = today.day

    # Handle ordinal suffixes with special cases for 11, 12, and 13.
    if 11 <= day % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return f"{today.strftime('%B')} {day}{suffix}, {today.year}"


if __name__ == "__main__":
    mcp.run(transport="stdio")