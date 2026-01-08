import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        # Validate path is inside working_directory
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists and is regular file
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # Check .py extension
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        # Build command
        command = ["python", target_path]
        if args:
            command.extend(args)
        
        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Build output
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")
        
        return "\n".join(output)
    
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments, 30s timeout, captures output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to Python file (.py) relative to working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command line arguments",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
