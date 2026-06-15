from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("classroom-remote-mcp", host="0.0.0.0", port=8000)


@mcp.tool()
def get_course(topic: str) -> dict:
    """Return a tiny course recommendation for a topic."""
    return {
        "topic": topic,
        "title": f"Introduction to {topic}",
        "duration_minutes": 20,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

