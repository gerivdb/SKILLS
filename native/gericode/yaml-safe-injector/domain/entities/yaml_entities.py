"""
DDD Entities — yaml-safe-injector
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class YamlFile:
    path: Path
    content: str = ""
    anchored: bool = False

    def load(self) -> None:
        self.content = self.path.read_text(encoding="utf-8")
        self.anchored = "&id" in self.content

    def has_anchors(self) -> bool:
        return self.anchored


@dataclass
class InjectionUpdate:
    key: str
    value: object
    repo_name: str

    def validate_repo_name(self) -> bool:
        return bool(self.repo_name and len(self.repo_name) > 0)
