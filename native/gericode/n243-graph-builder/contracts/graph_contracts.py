"""
DbC Contracts — n243-graph-builder
"""

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def non_empty_graph_contract(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        vertices = args[0] if args else kwargs.get("vertices")
        if not vertices:
            raise ValueError("Contract violation: graph must not be empty")
        return func(*args, **kwargs)

    return wrapper
