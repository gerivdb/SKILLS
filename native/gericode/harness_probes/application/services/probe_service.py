from __future__ import annotations

from typing import List

from harness_probes.application.ports.inbound.harness_probes_ports import ProbeInPort
from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO


class ProbeService:
    def __init__(self, out_port) -> None:
        self._out_port = out_port

    def run_all(self) -> List[ProbeResultVO]:
        from harness_probes.application.services.probes_impl import run_all
        results = run_all()
        for result in results:
            self._out_port.persist(result)
        return results






