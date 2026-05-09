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

@mcp.resource("info://currentdate")
def get_date() -> str:
    """Get current date."""
    return date.today().isoformat()


if __name__ == "__main__":
    mcp.run(transport="stdio")