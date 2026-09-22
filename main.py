import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse


def api_call(api_key: str, messages: list):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    return response


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Env OPENROUTER_API_KEY is None")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    response = api_call(api_key, messages)

    print(f"User Promt: {args.user_prompt}")

    if response.usage == None:
        tokens_promt: int | None = None
        tokens_response: int | None = None
    else:
        tokens_promt = response.usage.prompt_tokens
        tokens_response = response.usage.completion_tokens
    print(f"Prompt tokens: {tokens_promt}\nResponse tokens: {tokens_response}\nResponse:\n{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
