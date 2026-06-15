# Demo 2: Test with MCP Inspector

The Inspector lets learners see MCP messages without first building an agent.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
npx @modelcontextprotocol/inspector python server.py
```

Open the URL printed by Inspector, connect, and test these tabs:

1. **Tools**: call `grade` with `score=75`, then try `total=0`.
2. **Resources**: read `classroom://rules`.
3. **Prompts**: get `quiz_question` with `subject=MCP`.
4. **Notifications**: observe the protocol activity while making calls.

## What to point out

- Inspector discovers the server's capabilities first.
- Tool input fields come from the generated JSON schema.
- Resources are read, while tools are called.
- A prompt returns messages; it does not directly call an LLM.

