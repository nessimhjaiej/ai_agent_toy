
import os
from google.genai import types
"""- README.md: file_size=1032 bytes, is_dir=False
- src: file_size=128 bytes, is_dir=True
- package.json: file_size=1234 bytes, is_dir=False"""
def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = '.'
    #I opted for a try-except block to catch any unexpected errors . nothing complicated here
    try:
        #getting absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)
        #getting absolute path of target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False (if the target_dir is inside working_directory)
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir or not os.path.isdir(target_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        #if the target directory does not exist
        if not os.path.isdir(target_dir):
            return f'Error: The directory "{directory}" does not exist'
        #listing files and directories in target directory
        contents = os.listdir(target_dir)
        output = []
        #looping over the contents and getting their info
        for content in contents : 
            is_dir = os.path.isdir(os.path.join(target_dir, content))
            file_size = os.path.getsize(os.path.join(target_dir, content))
            output.append(f'- {content}: file_size={file_size} bytes, is_dir={is_dir}')
        return '\n'.join(output) if output else f'The directory "{directory}" is empty.'
    
    except Exception as e:
        return f'Error: {str(e)}'
    
        
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)