import os

def write_file(working_directory, file_path, content):
    source_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_path.startswith(source_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_path):
        return f'Error: target path points to existing directory, cannot overwrite'
    
    if not os.path.exists(os.path.dirname(target_path)):
        try:
            os.makedirs(os.path.dirname(target_path))
        except Exception as e:
            return f'Error: {e}'
    
    try:
        with open(target_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'