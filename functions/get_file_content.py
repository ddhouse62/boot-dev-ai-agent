import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    source_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(f'{source_path}/'):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_path, "r") as target:
            
            file_content_string = target.read()
            file_length = len(file_content_string)
            if file_length > 1000:
                return f'{file_content_string}...File "{file_path}" truncated at 10000 characters.'
            else:
                return file_content_string
    except Exception as e:
        print(f'Error: {e}')

