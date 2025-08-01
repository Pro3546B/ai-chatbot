import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check: File is inside working directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check: File exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        # Check: Is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Prepare command
        command = ["python", full_path] + args

        # Run subprocess with timeout, capturing output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        output_parts = []

        if result.stdout:
            output_parts.append(f'STDOUT:\n{result.stdout}')
        if result.stderr:
            output_parts.append(f'STDERR:\n{result.stderr}')
        if result.returncode != 0:
            output_parts.append(f'Process exited with code {result.returncode}')

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
