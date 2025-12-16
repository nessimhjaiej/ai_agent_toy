import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in .env or environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Usage: python main.py \"your prompt\" [--verbose]")
        sys.exit(1)

    prompt = sys.argv[1]
    verbose_flag = len(sys.argv) >= 3 and sys.argv[2] == "--verbose"

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
        )
    except errors.ClientError as e:
        print("Client error:", e)
        sys.exit(1)
    except Exception as e:
        print("Unexpected error:", e)
        sys.exit(1)

    if response is None or response.usage_metadata is None:
        print("Response is malformed :(")
        return

    print(response.text)

    if verbose_flag:
        print("usage_metadata prompt token count:", response.usage_metadata.prompt_token_count)
        print("usage_metadata candidates_token_count:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
