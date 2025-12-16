import os 
import subprocess

"""The stdout prefixed with STDOUT:, and stderr prefixed with STDERR:. 
The completed_process object has a stdout and stderr attribute."""
def run_python_file(working_directory, file_path, args=[]):
    try : 
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        valid = os.path.commonpath([abs_working_directory, abs_file_path]) == abs_working_directory
        if not valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith('.py'):
            return f'Error: File "{file_path}" is not a Python file.'
        completed_process = subprocess.run(['python', abs_file_path] + args, cwd=abs_working_directory, timeout=30, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        #0 means everything is fine :) 
        if completed_process.returncode != 0:
            return f'Error: Execution of "{file_path}" failed with return code {completed_process.returncode}.\nSTDERR: {completed_process.stderr.decode()}'
        #if no output is produced return "No output produced".
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        return f'STDOUT: {completed_process.stdout.decode()}\nSTDERR: {completed_process.stderr.decode()}'
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

