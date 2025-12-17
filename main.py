import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from functions.get_files_info import schema_get_files_info

def main():
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
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
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
    )


    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ), 
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
    if response.functions_calls:
        for fc in response.functions_calls:
            print(f"Calling function: {fc.name}({fc.args})")
    else : 
         print(response.text)
    if verbose_flag:
        print("usage_metadata prompt token count:", response.usage_metadata.prompt_token_count)
        print("usage_metadata candidates_token_count:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
