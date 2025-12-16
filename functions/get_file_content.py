import os
from pathlib import Path

def get_file_content(working_directory, file_path):
    try : 
        if file_path is None:
            return 'Error: No file path provided'
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_file_path = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        if not valid_file_path :
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        content = Path(abs_file_path).read_text(encoding='utf-8')
        # After reading the first MAX_CHARS...
        MAX_CHARS = 10000
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: {str(e)}'
    return content

    