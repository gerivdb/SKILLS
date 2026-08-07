"""
Hexagonal Infrastructure Adapters — yaml-safe-injector outbound
"""

from pathlib import Path
from typing import Protocol


class IFileSystemOutAdapter(Protocol):
    """Outbound adapter: filesystem operations."""

    def read_file(self, path: str) -> str:
        ...

    def write_file(self, path: str, content: str) -> None:
        ...

    def file_exists(self, path: str) -> bool:
        ...


class LocalFileSystemOutAdapter:
    """Local filesystem implementation."""

    def read_file(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")

    def file_exists(self, path: str) -> bool:
        return Path(path).exists()
