# LocalAI Python MCP

A small MCP server. Use at your own risk. Resources / Tools:
- an `exec` tool for executing Python snippets and returning output
- a `currentdate` resource for retrieving today's date

## Usage

Clone this repository:

```shell
git clone https://github.com/sstockdev/localai-python-mcp
```

Enter the project root and run with `uv`:

```shell
uv run main.py
```

The server runs over stdio, so it is intended to be launched by an MCP client.

## MCP Client Configuration

After cloning this repository, you can register it in your `mcp.json`:

```json
{
	"servers": {
		"localai-python-mcp": {
			"command": "uv",
			"args": [
				"run",
				"--directory",
				"FILEPATH_TO_PROJECT",
				"main.py"
			]
		}
	}
}
```

Replace `FILEPATH_TO_PROJECT` with the absolute path to this repository.

## Exposed MCP Interfaces

Tool:
- `exec(cmd: str) -> str`

Resource:
- `info://currentdate`

## Notes

- The `exec` tool runs arbitrary Python code. Only run this server in trusted environments.
