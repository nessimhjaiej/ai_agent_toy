import os 

def write_file(working_directory, file_path, content):
    try : 
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        valid_path = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path))
        else : 
            #overwrite 
            with open(abs_file_path, 'w') as file:
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
    