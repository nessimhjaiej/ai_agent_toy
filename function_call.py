from google import genai  # or: from google.genai import types
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = "calculator"

def call_function(function_call, verbose=False):
    if verbose:
        print(f'function name called: {function_call.name} with arguments: {function_call.args}')
    else: 
        print(f'function name called: {function_call.name}()')

    # mapping each function name to its implementation
    function_name = function_call.name
    args = function_call.args or {}

    if function_name == "get_files_info":
        function_result = get_files_info(working_directory, **args)
    elif function_name == "get_file_content":
        function_result = get_file_content(working_directory, **args)
    elif function_name == "write_file":
        function_result = write_file(working_directory, **args)
    elif function_name == "run_python_file":
        function_result = run_python_file(working_directory, **args)
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)

    # result is sent as a text to the model (LLM INPUT OUTPUT IS ONLY TEXT FOR NOW)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
