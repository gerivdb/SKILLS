from __future__ import annotations

from typing import List
from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO


class ProbeInPort:
    def run_all(self) -> List[ProbeResultVO]:
        raise NotImplementedError


class ProbeOutPort:
    def persist(self, result: ProbeResultVO) -> None:
        raise NotImplementedError
