"""
DbC Contracts — skill-scaffold
"""

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def skill_name_contract(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        name = args[0] if args else kwargs.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("Contract violation: skill name must be a non-empty string")
        return func(*args, **kwargs)

    return wrapper
