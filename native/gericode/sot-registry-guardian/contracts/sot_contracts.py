"""
DbC Contracts — sot-registry-guardian
"""

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def repo_name_contract(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        full_name = args[0] if args else kwargs.get("full_name")
        if not full_name or "/" not in str(full_name):
            raise ValueError("Contract violation: full_name must be owner/repo")
        return func(*args, **kwargs)

    return wrapper


def strate_contract(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        local_path = args[0] if args else kwargs.get("local_path")
        if not str(local_path).startswith("D:\\DO\\WEB\\TOOLS\\L"):
            raise ValueError("Contract violation: local_path must be under D:\\DO\\WEB\\TOOLS\\L<digit>")
        return func(*args, **kwargs)

    return wrapper
