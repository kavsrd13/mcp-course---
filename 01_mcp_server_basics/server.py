from mcp.server.fastmcp import FastMCP

mcp = FastMCP("classroom-basics")

COURSE_NOTES = {
    "tools": "Tools perform actions. The model decides when to call them.",
    "resources": "Resources expose data that a client can read as context.",
    "prompts": "Prompts are reusable message templates supplied by the server.",
}


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def attendance_message(student: str, present: bool = True) -> str:
    """Create a simple attendance message."""
    status = "present" if present else "absent"
    return f"{student} is marked {status}."


@mcp.resource("lesson://{topic}")
def lesson(topic: str) -> str:
    """Read a short lesson about an MCP primitive."""
    return COURSE_NOTES.get(topic, f"No lesson found for '{topic}'.")


@mcp.prompt()
def explain_for_beginner(topic: str) -> str:
    """Create a reusable teaching prompt."""
    return (
        f"Explain {topic} to a beginner. Use one analogy and one tiny example. "
        "Keep the answer under 150 words."
    )


if __name__ == "__main__":
    mcp.run()

