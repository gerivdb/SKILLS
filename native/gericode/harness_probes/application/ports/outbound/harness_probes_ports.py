from __future__ import annotations

from typing import List
from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO


class ProbeOutPort:
    def persist(self, result: ProbeResultVO) -> None:
        raise NotImplementedError

    def list_recent(self, limit: int = 20) -> List[ProbeResultVO]:
        raise NotImplementedError





