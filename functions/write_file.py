import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # Validate path is inside working_directory
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Check if target is a directory
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Create parent directories
        os.makedirs(os.path.dirname(target_path) or '.', exist_ok=True)
        
        # Write file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite file contents relative to working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file relative to working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)
