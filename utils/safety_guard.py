import os
from typing import List

# Simple denylist of dangerous command tokens; expand as needed
DANGEROUS_TOKENS: List[str] = [
    'rm', 'del', 'format', 'mkfs', 'netsh', 'shutdown', 'reboot',
    'diskpart', 'bcdedit', 'reg', 'powershell -EncodedCommand',
    'sudo', 'chmod 777', 'chown -R', 'bluetoothctl', 'iptables', 'ufw'
]

# Whitelisted base directory (user's home by default)
SAFE_BASE_DIR = os.path.expanduser('~')


def is_safe_command(text: str) -> bool:
    lower = (text or '').lower()
    return not any(tok in lower for tok in DANGEROUS_TOKENS)


def normalize_safe_path(path: str) -> str:
    """
    Normalize and ensure the path is inside SAFE_BASE_DIR.
    Raises ValueError if outside.
    """
    if not path:
        raise ValueError("Empty path")
    abspath = os.path.abspath(os.path.expanduser(path))
    base = os.path.abspath(SAFE_BASE_DIR)
    if os.path.commonpath([abspath, base]) != base:
        raise ValueError("Path outside of allowed directory")
    return abspath
