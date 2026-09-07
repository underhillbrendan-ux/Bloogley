import os


def is_path_safe(target_path: str, allowed_directories: list[str]) -> bool:
    """Checks whether target_path resides inside any of the allowed directories."""
    abs_target = os.path.abspath(target_path)
    for allowed in allowed_directories:
        abs_allowed = os.path.abspath(allowed)
        if os.path.commonpath([abs_allowed, abs_target]) == abs_allowed:
            return True
    return False