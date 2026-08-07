from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HarnessProbesContracts:
    expected_probe_count: int = 11
    expected_first_probe: str = "P-701"
    expected_last_probe: str = "P-711"
