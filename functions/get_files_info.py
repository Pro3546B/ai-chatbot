import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Convert to absolute paths
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        # Validate path is within working_directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Validate it's a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # List contents and build info string
        result_lines = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            try:
                file_size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                result_lines.append(f'- {item}: file_size={file_size} bytes, is_dir={is_dir}')
            except Exception as e:
                return f'Error: Could not access item "{item}": {e}'

        return '\n'.join(result_lines)

    except Exception as e:
        return f'Error: Failed to list directory "{directory}" due to: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
