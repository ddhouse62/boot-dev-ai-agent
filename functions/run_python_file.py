import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    source_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(source_path, file_path))
    
    if not target_path.startswith(source_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    
    if not target_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    process_args = ["python3", file_path]
    
    if len(args) != 0:
        process_args += args
    
    try:
        completed_process = subprocess.run(args = process_args, cwd = source_path, timeout = 30, capture_output = True)
        if completed_process.stdout == "" and completed_process.stderr == "":
            return "No output produced."
        
        output_string = f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}."
        
        if completed_process.returncode != 0:
            output_string += f" Process exited with code {output_string.returncode}"
        
        return output_string

    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with optional arguments in the current directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the appropriate python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional CLI args to pass to the Python file.",
                items = types.Schema(
                    type=types.Type.STRING,
                    description="A single argument"
                )
            ),
        },
        required=["file_path"]
    ),
)