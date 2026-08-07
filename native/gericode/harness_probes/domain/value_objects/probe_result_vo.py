from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProbeResultVO:
    probe_id: str
    passed: bool
    detail: Optional[str] = ""
