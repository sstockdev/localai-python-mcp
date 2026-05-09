"""
FastMCP quickstart example.

Run from the repository root:
    uv run main.py
"""

from datetime import date
import builtins
import io
import traceback
from contextlib import redirect_stdout

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("localai-python-mcp", json_response=True)

@mcp.tool()
def exec(cmd: str) -> str:
    """Execute python code and return the result."""
    if not cmd.strip():
        return ""

    namespace: dict[str, object] = {}
    stdout = io.StringIO()

    try:
        with redirect_stdout(stdout):
            try:
                result = builtins.eval(cmd, {}, namespace)
            except SyntaxError:
                builtins.exec(cmd, {}, namespace)
                result = None
    except Exception:
        return traceback.format_exc().strip()

    output = stdout.getvalue().rstrip("\n")
    if result is None:
        return output

    if output:
        return f"{output}\n{result}"
    return str(result)

@mcp.tool()
def get_date() -> str:
    """Return today's date in 'Month day-with-ordinal, year' format (e.g., 'May 9th, 2026')."""
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