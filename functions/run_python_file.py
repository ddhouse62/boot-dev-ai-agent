import os
import subprocess

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