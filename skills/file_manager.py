import os
from typing import Dict, Any, List, Optional
from utils.safety_guard import normalize_safe_path


ALLOWED_ACTIONS = {"list", "read", "create"}


def manage_files(action: str, path: str, content: Optional[str] = None) -> Dict[str, Any]:
    """
    Safe file operations limited to user's home directory:
    - list: list directory entries
    - read: read text file
    - create: create a new text file with provided content (or empty)
    """
    if action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported action")

    safe_path = normalize_safe_path(path)

    if action == "list":
        if not os.path.isdir(safe_path):
            raise FileNotFoundError("Directory not found")
        entries = sorted(os.listdir(safe_path))
        return {"path": safe_path, "entries": entries}

    if action == "read":
        if not os.path.isfile(safe_path):
            raise FileNotFoundError("File not found")
        with open(safe_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        return {"path": safe_path, "content": data}

    if action == "create":
        base_dir = os.path.dirname(safe_path)
        os.makedirs(base_dir, exist_ok=True)
        if os.path.exists(safe_path):
            raise FileExistsError("File already exists")
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content or "")
        return {"path": safe_path, "created": True}

    raise ValueError("Unhandled action")
