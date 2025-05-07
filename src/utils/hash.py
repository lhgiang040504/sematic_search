import hashlib
from typing import Any

from src.utils.serializer import to_json

def generate_md5_hash(args: Any) -> str:
    """Create a hash from the given arguments using MD5."""
    return hashlib.md5(to_json(args).encode()).hexdigest()