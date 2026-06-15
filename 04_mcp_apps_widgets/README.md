# Demo 4: MCP Apps Widgets

This demo teaches the MCP Apps pattern:

1. A tool returns data.
2. The tool points to a `ui://` resource.
3. The host loads that HTML resource in an iframe.
4. The widget receives the tool result and renders it.

One small vanilla-JavaScript UI handles three tools:

- `show_time`
- `show_weather` using the free Open-Meteo API
- `show_calendar`

## Run

```powershell
npm install
npm start
```

The MCP endpoint is `http://localhost:3001/mcp`.

Use an MCP Apps-compatible host. For the official example host, clone
`https://github.com/modelcontextprotocol/ext-apps`, run `npm install` and
`npm start`, then open `http://localhost:8080`.

Try prompts such as:

- "Show the time at UTC+05:30."
- "Show the weather in Bengaluru."
- "Show a calendar for June 2026."

