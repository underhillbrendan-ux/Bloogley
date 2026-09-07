import os
from functions.security import is_path_safe
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory, providing file size and directory status.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from.",
                },
            },
            "required": ["directory"],
        },
    },
}


def get_files_info(allowed_directories: list[str], directory: str = ".") -> str:
    try:
        if not is_path_safe(directory, allowed_directories):
            return f'Error: Cannot list "{directory}" as it is outside permitted directories'

        target_dir = os.path.abspath(directory)

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(target_dir)
        lines = []

        for item in items:
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(lines) if lines else "Directory is empty."

    except Exception as e:
        return f"Error: {e}"
