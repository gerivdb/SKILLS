"""
Hexagonal Infrastructure Adapters — sot-registry-guardian outbound
"""

from pathlib import Path
from typing import Protocol


class ISOTFileSystemAdapter(Protocol):
    """Outbound adapter: SOT filesystem."""

    def read_sot(self, path: str) -> str:
        ...

    def write_sot(self, path: str, content: str) -> None:
        ...


class LocalSOTFileSystemAdapter:
    """Local filesystem implementation for SOT."""

    def read_sot(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write_sot(self, path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")
