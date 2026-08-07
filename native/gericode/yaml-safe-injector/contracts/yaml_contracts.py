"""
DbC Contracts — yaml-safe-injector
"""

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def yaml_path_contract(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        target = args[0] if args else kwargs.get("target_path")
        from pathlib import Path
        if isinstance(target, Path) and target.suffix != ".yaml":
            raise ValueError("Contract violation: target_path must be .yaml")
        return func(*args, **kwargs)

    return wrapper


def dry_run_contract(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        dry_run = kwargs.get("dry_run", False)
        if dry_run:
            raise RuntimeError("Contract violation: dry_run must not modify file")
        return func(*args, **kwargs)

    return wrapper
