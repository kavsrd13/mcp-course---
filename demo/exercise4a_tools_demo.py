import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import AzureOpenAI


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_weather(city: str) -> str:
    sample = {
        "seattle": "18C, cloudy",
        "london": "14C, light rain",
        "hyderabad": "31C, sunny",
        "new york": "22C, clear",
    }
    return sample.get(city.strip().lower(), "Weather data not found for that city.")


def run_tool_call(tool_name: str, arguments_json: str) -> str:
    args: dict[str, Any] = json.loads(arguments_json or "{}")
    if tool_name == "get_weather":
        city = str(args.get("city", ""))
        return get_weather(city)
    return "Unsupported tool call."


def main() -> None:
    load_dotenv()

    endpoint = require_env("AZURE_OPENAI_ENDPOINT")
    api_key = require_env("AZURE_OPENAI_API_KEY")
    deployment = require_env("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for a given city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name to query",
                        }
                    },
                    "required": ["city"],
                },
            },
        }
    ]

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can use tools when needed.",
        }
    ]

    print("Exercise 4A Demo: Generative AI App That Uses Tools")
    print("Ask a weather question like: 'What is the weather in Seattle?'")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        messages.append({"role": "user", "content": user_input})

        first = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )

        first_message = first.choices[0].message
        tool_calls = first_message.tool_calls or []

        if not tool_calls:
            answer = first_message.content or ""
            print(f"Assistant: {answer}\n")
            messages.append({"role": "assistant", "content": answer})
            continue

        assistant_msg: dict[str, Any] = {
            "role": "assistant",
            "content": first_message.content,
            "tool_calls": [call.model_dump() for call in tool_calls],
        }
        messages.append(assistant_msg)

        for call in tool_calls:
            result = run_tool_call(call.function.name, call.function.arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": call.function.name,
                    "content": result,
                }
            )

        final = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=0.2,
        )

        final_answer = final.choices[0].message.content or ""
        print(f"Assistant: {final_answer}\n")
        messages.append({"role": "assistant", "content": final_answer})


if __name__ == "__main__":
    main()
