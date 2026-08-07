"""
Hexagonal Adapters — yaml-safe-injector
"""

from pathlib import Path
from typing import Protocol


class LocalFileSystemAdapter:
    """Outbound adapter: local filesystem."""

    def read(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write(self, path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")

    def exists(self, path: str) -> bool:
        return Path(path).exists()


class YamlInjectorService:
    """Application service orchestrating injection."""

    def __init__(self, fs: LocalFileSystemAdapter) -> None:
        self.fs = fs

    def inject(
        self,
        target_path: str,
        updates: dict,
        repo_name: str,
        dry_run: bool = False,
    ) -> tuple[str, str]:
        content = self.fs.read(target_path)
        # minimal placeholder: real injection is in yaml_safe_injector.py
        if not dry_run:
            self.fs.write(target_path, content)
        return target_path, ""
