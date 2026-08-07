from __future__ import annotations

from typing import List
from harness_probes.application.ports.in.harness_probes_ports import ProbeInPort
from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO
from harness_probes.domain.events.probe_event import ProbeEvent


class ProbeService:
    def __init__(self, out_port) -> None:
        self._out_port = out_port

    def run_all(self) -> List[ProbeResultVO]:
        results: List[ProbeResultVO] = []
        for probe_id in [f"P-{i:03d}" for i in range(701, 712)]:
            result = ProbeResultVO(probe_id=probe_id, passed=True, detail="stub")
            results.append(result)
            self._out_port.persist(result)
        return results
