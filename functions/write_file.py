import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    try : 
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        valid_path = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # ensure parent directories exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # overwrite or create the file
        with open(abs_file_path, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_write_file = types.FunctionDeclaration(
    
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
