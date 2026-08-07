from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProbeResultEntity:
    probe_id: str
    passed: bool
    detail: str = ""
