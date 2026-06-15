# Demo 3: Azure OpenAI Agent with an MCP Tool

The OpenAI SDK sends a request to your Azure-hosted model deployment. The model
can discover and call tools from the remote MCP server.

## 1. Start the MCP server

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

The local endpoint is `http://localhost:8000/mcp`.

Azure cannot call your laptop's `localhost`. For a classroom demo, expose the
server with a tunnel such as dev tunnels or ngrok, then use its HTTPS `/mcp` URL.

## 2. Configure Azure OpenAI

```powershell
$env:AZURE_OPENAI_API_KEY="your-key"
$env:AZURE_OPENAI_BASE_URL="https://YOUR-RESOURCE.openai.azure.com/openai/v1/"
$env:AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
$env:MCP_SERVER_URL="https://YOUR-PUBLIC-URL/mcp"
python agent.py
```

The important line is the `{"type": "mcp", ...}` tool definition. Azure uses the
deployment name in `model`, discovers the remote server, and lets the model call
`get_course`.

