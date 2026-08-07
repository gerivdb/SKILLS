from __future__ import annotations

from typing import Iterable, List
from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO
from harness_probes.domain.repository_contracts.probe_repo import ProbeRepositoryContract


class InMemoryProbeRepository(ProbeRepositoryContract):
    def __init__(self) -> None:
        self._items: List[ProbeResultVO] = []

    def persist(self, result: ProbeResultVO) -> None:
        self._items.append(result)

    def list_recent(self, limit: int = 20) -> Iterable[ProbeResultVO]:
        return list(self._items[-limit:])





