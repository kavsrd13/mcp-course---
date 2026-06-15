import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import cors from "cors";
import fs from "node:fs/promises";
import path from "node:path";
import { z } from "zod";

const resourceUri = "ui://classroom/widgets.html";

function createServer() {
  const server = new McpServer({ name: "classroom-widgets", version: "1.0.0" });

  const ui = { _meta: { ui: { resourceUri } } };

  registerAppTool(server, "show_time", {
    title: "Show Time",
    description: "Show the current time for a UTC offset such as +05:30.",
    inputSchema: { utcOffset: z.string().default("+00:00") },
    ...ui,
  }, async ({ utcOffset }) => ({
    structuredContent: {
      widget: "time",
      title: `Time at UTC${utcOffset}`,
      value: timeAtOffset(utcOffset),
    },
    content: [{ type: "text", text: `Current time for UTC${utcOffset}` }],
  }));

  registerAppTool(server, "show_calendar", {
    title: "Show Calendar",
    description: "Show a simple calendar for a month.",
    inputSchema: {
      year: z.number().int().min(2000).max(2100),
      month: z.number().int().min(1).max(12),
    },
    ...ui,
  }, async ({ year, month }) => ({
    structuredContent: {
      widget: "calendar",
      title: new Date(year, month - 1).toLocaleString("en", {
        month: "long",
        year: "numeric",
      }),
      year,
      month,
    },
    content: [{ type: "text", text: `Calendar for ${year}-${month}` }],
  }));

  registerAppTool(server, "show_weather", {
    title: "Show Weather",
    description: "Show current weather for a city using the free Open-Meteo API.",
    inputSchema: { city: z.string().default("Bengaluru") },
    ...ui,
  }, async ({ city }) => {
    const place = await fetch(
      `https://geocoding-api.open-meteo.com/v1/search?count=1&name=${encodeURIComponent(city)}`,
    ).then((response) => response.json()) as any;
    const location = place.results?.[0];
    if (!location) {
      return { content: [{ type: "text", text: `City not found: ${city}` }], isError: true };
    }

    const weather = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${location.latitude}&longitude=${location.longitude}&current=temperature_2m,wind_speed_10m`,
    ).then((response) => response.json()) as any;

    return {
      structuredContent: {
        widget: "weather",
        title: location.name,
        temperature: weather.current.temperature_2m,
        wind: weather.current.wind_speed_10m,
      },
      content: [{ type: "text", text: `Current weather in ${location.name}` }],
    };
  });

  registerAppResource(
    server,
    resourceUri,
    resourceUri,
    { mimeType: RESOURCE_MIME_TYPE },
    async () => ({
      contents: [{
        uri: resourceUri,
        mimeType: RESOURCE_MIME_TYPE,
        text: await fs.readFile(path.join(import.meta.dirname, "dist", "widget.html"), "utf8"),
      }],
    }),
  );

  return server;
}

function timeAtOffset(offset: string) {
  const match = offset.match(/^([+-])(\d{2}):(\d{2})$/);
  if (!match) return "Invalid UTC offset";

  const direction = match[1] === "+" ? 1 : -1;
  const minutes = direction * (Number(match[2]) * 60 + Number(match[3]));
  return new Date(Date.now() + minutes * 60_000).toLocaleTimeString("en-US", {
    timeZone: "UTC",
  });
}

const app = createMcpExpressApp({ host: "0.0.0.0" });
app.use(cors());
app.all("/mcp", async (req, res) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(3001, () => {
  console.log("MCP Apps server: http://localhost:3001/mcp");
});
