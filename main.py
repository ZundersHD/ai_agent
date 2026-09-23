import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

from prompts import system_prompt
from call_function import available_functions


def api_call(api_key: str, messages: list):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    return response


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Env OPENROUTER_API_KEY is None")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    response = api_call(api_key, messages)
    message = response.choices[0].message

    if response.usage == None:
        tokens_promt: int | None = None
        tokens_response: int | None = None
    else:
        tokens_promt = response.usage.prompt_tokens
        tokens_response = response.usage.completion_tokens

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {tokens_promt}")
        print(f"Response tokens: {tokens_response}")

    print(message.content)

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}") # pyright: ignore[reportAttributeAccessIssue]
            print(f"Calling function: {tool_call.function.name}({function_args})") # pyright: ignore[reportAttributeAccessIssue]

if __name__ == "__main__":
    main()
