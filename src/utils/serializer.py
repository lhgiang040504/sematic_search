import json
from enum import Enum
from typing import Any

from pydantic import BaseModel

def serialize(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return serialize(obj.model_dump())
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, list):
        return [serialize(item) for item in obj]
    if isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    if isinstance(obj, set):
        return sorted(serialize(item) for item in obj)  # Sort to ensure consistent ordering
    if isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}
    if isinstance(obj, type):
        return obj.__name__
    if hasattr(obj, '__dict__'):
        return serialize(vars(obj))
    return str(obj)  # Fallback to string representation


def to_json(obj) -> str:
    # if isinstance(obj, BaseModel):
    #     return obj.model_dump_json(indent=2)
    # else:
    return json.dumps(serialize(obj), indent=2, default=str, ensure_ascii=False)


if __name__ == "__main__":
    
    class User(BaseModel):
        id: int
        name: str

    user = User(id=1, name="Alice")
    print(to_json(user))
    
    class Role(Enum):
        ADMIN = "admin"
        USER = "user"

    data = {"name": "Alice", "role": Role.ADMIN, "tags": {"python", "ai"}}
    print(to_json(data))
