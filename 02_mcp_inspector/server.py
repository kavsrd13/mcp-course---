from mcp.server.fastmcp import FastMCP

mcp = FastMCP("inspector-lab")


@mcp.tool()
def grade(score: int, total: int = 100) -> dict:
    """Return a percentage and a simple pass/fail result."""
    if total <= 0:
        return {"error": "total must be greater than zero"}

    percentage = round(score / total * 100, 1)
    return {"percentage": percentage, "passed": percentage >= 40}


@mcp.resource("classroom://rules")
def classroom_rules() -> str:
    """Return sample classroom rules."""
    return "1. Ask questions\n2. Try the tool\n3. Explain what happened"


@mcp.prompt()
def quiz_question(subject: str, level: str = "beginner") -> str:
    """Create a prompt for generating one quiz question."""
    return (
        f"Create one {level} multiple-choice question about {subject}. "
        "Include four choices and identify the correct answer."
    )


if __name__ == "__main__":
    mcp.run()

