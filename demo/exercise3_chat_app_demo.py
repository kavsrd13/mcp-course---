import os

from dotenv import load_dotenv
from openai import AzureOpenAI


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


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

    messages = [
        {
            "role": "system",
            "content": "You are a concise teaching assistant for Azure AI workshops.",
        }
    ]

    print("Exercise 3 Demo: Generative AI Chat App")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=0.4,
            max_tokens=500,
        )

        reply = response.choices[0].message.content or ""
        print(f"Assistant: {reply}\n")
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
