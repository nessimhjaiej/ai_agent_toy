import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from function_call import call_function
def main():
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

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
    
  
   
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
    )
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
    max_iter = 20 
    for i in range (0, max_iter) :
            
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

        if verbose_flag:
            print("usage_metadata prompt token count:", response.usage_metadata.prompt_token_count)
            print("usage_metadata candidates_token_count:", response.usage_metadata.candidates_token_count)



        for candidate in response.candidates:
            if candidate is None or candidate.content is None : 
                print("Candidate or candidate content is malformed :(")
                sys.exit(1)
            else : 
                messages.append(candidate.content) 
                

        if response.function_calls:
            for fc in response.function_calls:
                result = call_function(fc, verbose=verbose_flag)
                messages.append(
                    types.Content(
                        role="tool",  # Note: The role for function outputs is usually "tool"
                        parts=[
                            types.Part.from_function_response(
                                name=fc.name,
                                response={"result": result},  # The result must be a dictionary
                            )
                        ],
                    )
                )
            # Skip printing partial responses that contain function calls to avoid warnings.
            continue

        # Check if there is actual text to print
        if response.text is not None and response.text.strip() != "":
            print("Final Response from AI Agent:")
            print(response.text)
            return



if __name__ == "__main__":
    main()
