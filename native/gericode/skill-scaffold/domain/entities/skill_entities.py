"""
DDD Entities — skill-scaffold
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillSpec:
    name: str
    citizen: str
    layer: str
    description: str = ""

    def is_valid_name(self) -> bool:
        return bool(self.name and "-" in self.name)
