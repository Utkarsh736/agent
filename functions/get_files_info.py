import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Get absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Validate target is inside working_directory
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if target is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # List directory contents
        items = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
                size_str = f"{size} bytes" if not is_dir else f"{size} bytes"
            except OSError:
                size_str = "unknown size"
            items.append(f"- {item}: file_size={size_str}, is_dir={is_dir}")
        
        header = f"Result for '{directory}' directory:" if directory != "." else "Result for current directory:"
        return f"{header}\n" + "\n".join(items)
    
    except Exception as e:
        return f"Error: {str(e)}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

