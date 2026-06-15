import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    base_url=os.environ["AZURE_OPENAI_BASE_URL"],
)

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    input="Suggest a short course for learning MCP. Use the course server.",
    tools=[
        {
            "type": "mcp",
            "server_label": "classroom_courses",
            "server_url": os.environ["MCP_SERVER_URL"],
            "require_approval": "never",
        }
    ],
)

print(response.output_text)

