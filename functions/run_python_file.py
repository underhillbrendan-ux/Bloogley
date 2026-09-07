import os
import subprocess
from functions.security import is_path_safe
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file with optional command-line arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python script to execute.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the script.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    allowed_directories: list[str], file_path: str, args: list[str] | None = None
) -> str:
    try:
        # Check script path security bounds
        if not is_path_safe(file_path, allowed_directories):
            return f'Error: Cannot execute "{file_path}" as it is outside permitted directories'

        target_path = os.path.abspath(file_path)

        # Check existence and regular file status
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check .py extension
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Set working directory to the script's directory (ensures subprocess stays contained)
        execution_cwd = os.path.dirname(target_path)

        # Build command list
        command = ["python", target_path]
        if args:
            command.extend(args)

        # Execute process
        result = subprocess.run(
            command,
            cwd=execution_cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        # Check return code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # Check stdout & stderr
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error executing Python file: {e}"