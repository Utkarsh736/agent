import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Validate path is inside working_directory
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if it's a file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file with limit
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            # Check if truncated
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
    
    except Exception as e:
        return f"Error: {str(e)}"

