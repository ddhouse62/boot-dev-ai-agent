import os
from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a given file's content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the content to be written/overwritten, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write/overwrite into the file provided by file_path.  Required parameter."
            )
        },
    ),
)