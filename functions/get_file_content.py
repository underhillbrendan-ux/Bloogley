import os
from config import MAX_CHARS
from functions.security import is_path_safe

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the contents of a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read.",
                }
            },
            "required": ["file_path"],
        },
    },
}



def get_file_content(allowed_directories: list[str], file_path: str) -> str:
    try:
        if not is_path_safe(file_path, allowed_directories):
            return f'Error: Cannot read "{file_path}" as it is outside permitted directories'

        target_path = os.path.abspath(file_path)

        # Ensure target is a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read content up to MAX_CHARS + truncation check
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f'Error: {str(e)}'