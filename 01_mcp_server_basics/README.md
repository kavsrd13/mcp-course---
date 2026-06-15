# Demo 1: MCP Server Basics

This one file shows the three main server primitives:

- **Tool**: an action, such as adding numbers.
- **Resource**: data, such as a lesson note.
- **Prompt**: a reusable prompt template.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

`mcp.run()` uses the local `stdio` transport by default. An MCP client starts the
process and communicates with it through standard input/output.

## Teaching ideas

1. Change the description of `add` and observe how tool metadata changes.
2. Read `lesson://tools`, `lesson://resources`, and `lesson://prompts`.
3. Add a new tool using another `@mcp.tool()` decorator.

