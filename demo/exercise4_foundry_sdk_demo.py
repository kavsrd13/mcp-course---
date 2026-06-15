import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    load_dotenv()

    endpoint = require_env("AZURE_AI_FOUNDRY_ENDPOINT")
    api_key = require_env("AZURE_AI_FOUNDRY_API_KEY")
    model_name = require_env("AZURE_AI_FOUNDRY_MODEL")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    history = [
        SystemMessage(content="You are an Azure AI Foundry demo assistant.")
    ]

    print("Exercise 4 Demo: Create a Generative AI Chat App (Foundry SDK)")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        history.append(UserMessage(content=user_input))

        response = client.complete(
            model=model_name,
            messages=history,
            temperature=0.3,
            max_tokens=400,
        )

        reply = response.choices[0].message.content or ""
        print(f"Assistant: {reply}\n")
        history.append(AssistantMessage(content=reply))


if __name__ == "__main__":
    main()
